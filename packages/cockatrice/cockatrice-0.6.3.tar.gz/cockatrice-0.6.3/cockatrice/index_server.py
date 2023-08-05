# -*- coding: utf-8 -*-

# Copyright (c) 2018 Minoru Osuka
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# 		http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import functools
import os
import re
import threading
import time
import zipfile
from logging import getLogger

import pysyncobj.pickle as pickle
from pysyncobj import replicated, SyncObj, SyncObjConf
from whoosh.filedb.filestore import FileStorage
from whoosh.qparser import QueryParser


class IndexServer(SyncObj):
    def __init__(self, host='localhost', port=7070, peer_addrs=[], conf=SyncObjConf(),
                 index_dir='/tmp/cockatrice/index', logger=getLogger()):
        self.__logger = logger

        self.__lock = threading.RLock()

        self.__bind_addr = '{0}:{1}'.format(host, port)
        self.__peer_addrs = peer_addrs
        self.__index_dir = index_dir
        self.__conf = conf
        self.__conf.serializer = self.__serialize
        self.__conf.deserializer = self.__deserialize
        self.__conf.validate()

        self.__indices = {}

        self.__file_storage = None

        self.__logger.info('starting index server: {0}, {1}'.format(self.__bind_addr, self.__peer_addrs))

        self.__logger.info('creating file storage for indices on {0}'.format(self.__index_dir))
        os.makedirs(self.__index_dir, exist_ok=True)
        self.__file_storage = FileStorage(self.__index_dir, supports_mmap=True, readonly=False, debug=False)

        super(IndexServer, self).__init__(self.__bind_addr, self.__peer_addrs, conf=self.__conf)

        self.__logger.info('index server started')

        # open existing indices on startup
        self.__logger.info('opening existing indices')
        self.__open_existing_indices()
        self.__logger.info('existing indices opened')

        # waiting for the preparation to be completed
        while not self.isReady():
            # recovering data
            self.__logger.info('waiting for the cluster to be ready')
            time.sleep(1)
        self.__logger.info('the index server is ready')

    def stop(self):
        self.__logger.info('stopping index server')
        for index_name in self.__indices.keys():
            self.close_index(index_name)
        self.destroy()
        self.__logger.info('index server stopped')

    def destroy(self):
        super().destroy()

    def __onUtilityMessage(self, conn, message):
        try:
            if message[0] == 'status':
                conn.send(self.getStatus())
                return True
            elif message[0] == 'add':
                self.addNodeToCluster(message[1],
                                      callback=functools.partial(self.__utilityCallback, conn=conn, cmd='ADD',
                                                                 node=message[1]))
                return True
            elif message[0] == 'remove':
                if message[1] == self.__selfNodeAddr:
                    conn.send('FAIL REMOVE ' + message[1])
                else:
                    self.removeNodeFromCluster(message[1], callback=functools.partial(self.__utilityCallback, conn=conn,
                                                                                      cmd='REMOVE', node=message[1]))
                return True
            elif message[0] == 'set_version':
                self.setCodeVersion(message[1],
                                    callback=functools.partial(self.__utilityCallback, conn=conn, cmd='SET_VERSION',
                                                               node=str(message[1])))
                return True
            elif message[0] == 'get_snapshot':
                with open(self.__conf.fullDumpFile, 'rb') as f:
                    conn.send(f.read())
                return True
        except Exception as e:
            conn.send(str(e))
            return True

    def __serialize(self, filename, raft_data):
        self.__logger.info('creating snapshot file: {0}'.format(filename))
        try:
            with self.__lock:
                with zipfile.ZipFile(filename, 'w', zipfile.ZIP_DEFLATED) as f:
                    for index_filename in self.__file_storage:
                        abs_index_path = os.path.join(self.__file_storage.folder, index_filename)
                        self.__logger.info('storing index file: {0}'.format(abs_index_path))
                        f.write(abs_index_path, index_filename)
                    self.__logger.info('storing raft transaction log')
                    f.writestr('raft.bin', pickle.dumps(raft_data))
                self.__logger.info('snapshot file created: {0}'.format(filename))
        except Exception as ex:
            self.__logger.error(ex)

    def __deserialize(self, filename):
        self.__logger.info('restoring from snapshot: {0}'.format(self.__conf.fullDumpFile))
        try:
            with self.__lock:
                self.__logger.info('cleaning {0}'.format(self.__file_storage.folder))
                self.__file_storage.destroy()
                self.__file_storage.create()

                with zipfile.ZipFile(filename, 'r') as f:
                    for member in f.namelist():
                        if member != 'raft.bin':
                            self.__logger.info(
                                'restoring {0}'.format(os.path.join(self.__file_storage.folder, member)))
                            f.extract(member, path=self.__file_storage.folder)
                    return pickle.loads(f.read('raft.bin'))
        except Exception as ex:
            self.__logger.error(ex)

    def get_file_storage(self):
        return self.__file_storage

    def __index_exists(self, index_name):
        return self.__file_storage.index_exists(indexname=index_name)

    def __get_existing_index_names(self):
        index_names = []

        pattern_toc = re.compile('^_(.+)_\\d+\\.toc$')
        self.__logger.info('seeking indices on {0}'.format(self.__file_storage.folder))
        for filename in self.__file_storage:
            match = pattern_toc.search(filename)
            if match:
                self.__logger.debug(
                    '{0} found in file storage on {1}'.format(match.group(1), self.__file_storage.folder))
                index_names.append(match.group(1))

        return index_names

    def __open_existing_indices(self):
        for index_name in self.__get_existing_index_names():
            self.open_index(index_name, schema=None, _doApply=False)

    @replicated
    def open_index(self, index_name, schema=None):
        index = None

        try:
            self.__logger.info('opening {0} in file storage on {1}'.format(index_name, self.__file_storage.folder))
            if not self.__index_exists(index_name):
                raise KeyError(
                    '{0} does not exist in file storage on {1}'.format(index_name, self.__file_storage.folder))
            if index_name in self.__indices:
                index = self.__indices[index_name]
                self.__logger.info(
                    '{0} in file storage on {1} already opened'.format(index_name, self.__file_storage.folder))
            else:
                index = self.__file_storage.open_index(indexname=index_name, schema=schema)
                self.__indices[index_name] = index
                self.__logger.info('{0} in file storage on {1} opened'.format(index_name, self.__file_storage.folder))
        except Exception as ex:
            self.__logger.info(
                'failed to open {0} in file storage on {1}: {2}'.format(index_name, self.__file_storage.folder, ex))

        return index

    @replicated
    def close_index(self, index_name):
        try:
            index = self.__indices.pop(index_name)
            self.__logger.info('closing {0} in file storage on {1}'.format(index_name, index.storage.folder))
            if index is None:
                raise KeyError('{0} in file storage on {1} already closed'.format(index_name, index.storage.folder))
            else:
                index.close()
            self.__logger.info('{0} in file storage on {1} closed'.format(index_name, index.storage.folder))
        except Exception as ex:
            self.__logger.error(
                'failed to close {0} in file storage on {1}: {2}'.format(index_name, index.storage.folder, ex))

        return index

    @replicated
    def create_index(self, index_name, schema):
        index = None

        try:
            if self.__index_exists(index_name):
                self.open_index(index_name, schema=schema, _doApply=True)
            else:
                self.__logger.info('creating {0} in file storage on {1}'.format(index_name, self.__file_storage.folder))
                self.__indices[index_name] = self.__file_storage.create_index(schema, indexname=index_name)
                index = self.__indices[index_name]
                self.__logger.info('{0} in file storage on {1} created'.format(index_name, self.__file_storage.folder))
        except Exception as ex:
            self.__logger.error(
                'failed to close {0} in file storage on {1}: {2}'.format(index_name, self.__file_storage.folder, ex))

        return index

    @replicated
    def delete_index(self, index_name):
        success = False

        # close index
        self.close_index(index_name, _doApply=True)

        # delete index files
        try:
            self.__logger.info('deleting {0} in file storage on {1}'.format(index_name, self.__file_storage.folder))
            pattern_toc = re.compile('^_{0}_(\\d+)\\.toc$'.format(index_name))
            for filename in self.__file_storage:
                if re.match(pattern_toc, filename):
                    self.__logger.info('deleting {0}'.format(os.path.join(self.__file_storage.folder, filename)))
                    self.__file_storage.delete_file(filename)
            pattern_seg = re.compile('^{0}_([a-z0-9]+)\\.seg$'.format(index_name))
            for filename in self.__file_storage:
                if re.match(pattern_seg, filename):
                    self.__logger.info('deleting {0}'.format(os.path.join(self.__file_storage.folder, filename)))
                    self.__file_storage.delete_file(filename)
            pattern_lock = re.compile('^{0}_WRITELOCK$'.format(index_name))
            for filename in self.__file_storage:
                if re.match(pattern_lock, filename):
                    self.__logger.info('deleting {0}'.format(os.path.join(self.__file_storage.folder, filename)))
                    self.__file_storage.delete_file(filename)
            success = True
            self.__logger.info('{0} in file storage on {1} deleted'.format(index_name, self.__file_storage.folder))
        except Exception as ex:
            self.__logger.error(
                'failed to delete {0} in file storage on {1}: {2}'.format(index_name, self.__file_storage.folder, ex))

        return success

    def get_indices(self):
        return self.__indices

    def get_index(self, index_name):
        index = self.get_indices().get(index_name)
        if index is None:
            msg = '{0} is not available'.format(index_name)
            self.__logger.error(msg)
            raise KeyError(msg)
        return index

    @replicated
    def optimize_index(self, index_name):
        success = False

        try:
            index = self.get_index(index_name)
            self.__logger.info('optimizing {0} in file storage on {1}'.format(index_name, index.storage.folder))
            index.optimize()
            success = True
            self.__logger.info('{0} in file storage on {1} optimized'.format(index_name, index.storage.folder))
        except Exception as ex:
            self.__logger.error('failed to optimize {0}: {1}'.format(index_name, ex))

        return success

    def get_doc_count(self, index_name):
        try:
            cnt = self.get_index(index_name).doc_count()
        except Exception as ex:
            self.__logger.error('failed to get document count in {0}'.format(index_name))
            raise ex

        return cnt

    def get_writer(self, index_name):
        try:
            writer = self.get_index(index_name).writer()
        except Exception as ex:
            self.__logger.error('failed to get index writer in {0}'.format(index_name))
            raise ex

        return writer

    def get_schema(self, index_name):
        try:
            schema = self.get_index(index_name).schema
        except Exception as ex:
            self.__logger.error('failed to get index schema in {0}'.format(index_name))
            raise ex

        return schema

    def get_searcher(self, index_name, weighting=None):
        try:
            if weighting is None:
                searcher = self.get_index(index_name).searcher()
            else:
                searcher = self.get_index(index_name).searcher(weighting=weighting)
        except Exception as ex:
            self.__logger.error('failed to get index searcher in {0}'.format(index_name))
            raise ex

        return searcher

    @replicated
    def put_document(self, index_name, doc_id, fields):
        success = False

        try:
            self.__logger.debug('putting document in {0}: {1} {2}'.format(index_name, doc_id, fields))

            writer = self.get_writer(index_name)
            doc = {
                self.get_schema(index_name).get_unique_field(): doc_id
            }
            doc.update(fields)
            try:
                writer.update_document(**doc)
                success = True
            except Exception as ex:
                self.__logger.error('failed to put document in {0}: {1}'.format(index_name, doc))
                raise ex
            finally:
                if success:
                    writer.commit()
                else:
                    writer.cancel()
        except Exception as ex:
            self.__logger.error('failed to index document in {0}: {1}'.format(index_name, ex))

        return success

    @replicated
    def delete_document(self, index_name, doc_id):
        success = False

        try:
            self.__logger.debug('deleting document in {0}: {1}'.format(index_name, doc_id))

            unique_field = self.get_schema(index_name).get_unique_field()
            writer = self.get_writer(index_name)
            try:
                writer.delete_by_term(unique_field, doc_id)
                success = True
            except Exception as ex:
                self.__logger.error('failed to delete document in {0}: {1}:{2}'.format(index_name, unique_field,
                                                                                       doc_id))
                raise ex
            finally:
                if success:
                    writer.commit()
                else:
                    writer.cancel()
        except Exception as ex:
            self.__logger.error('failed to delete document in {0}: {1}'.format(index_name, ex))

        return success

    @replicated
    def put_documents(self, index_name, docs):
        cnt = 0

        try:
            success = False
            writer = self.get_writer(index_name)
            try:
                for doc in docs:
                    self.__logger.debug('indexing document in {0}: {1}'.format(index_name, doc))
                    writer.update_document(**doc)
                    cnt = cnt + 1
                success = True
            except Exception as ex:
                self.__logger.error('failed to index documents in {0} in bulk'.format(index_name))
                raise ex
            finally:
                if success:
                    writer.commit()
                else:
                    cnt = 0  # clear
                    writer.cancel()
        except Exception as ex:
            self.__logger.error('failed to index documents in {0} in bulk: {1}'.format(index_name, ex))

        return cnt

    @replicated
    def delete_documents(self, index_name, doc_ids):
        cnt = 0

        try:
            success = False
            writer = self.get_writer(index_name)
            unique_field = self.get_schema(index_name).get_unique_field()
            try:
                for doc_id in doc_ids:
                    self.__logger.debug('deleting document in {0}: {1}:{2}'.format(index_name, unique_field, doc_id))
                    writer.delete_by_term(unique_field, doc_id)
                    cnt = cnt + 1
                success = True
            except Exception as ex:
                self.__logger.error('failed to delete documents in {0} in bulk'.format(index_name))
                raise ex
            finally:
                if success:
                    writer.commit()
                else:
                    cnt = 0  # clear
                    writer.cancel()
        except Exception as ex:
            self.__logger.error('failed to delete documents in {0} in bulk: {1}'.format(index_name, ex))

        return cnt

    def get_document(self, index_name, doc_id):
        try:
            unique_field = self.get_schema(index_name).get_unique_field()
            try:
                self.__logger.debug('getting document in {0}: {1}:{2}'.format(index_name, unique_field, doc_id))
                doc = self.search_documents(index_name, doc_id, unique_field, 1, page_len=1)
            except Exception as ex:
                self.__logger.error('failed to get document in {0}: {1}:{2}'.format(index_name, unique_field, doc_id))
                raise ex
        except Exception as ex:
            self.__logger.error('failed to get document in {0}'.format(index_name))
            raise ex

        return doc

    def search_documents(self, index_name, query, search_field, page_num, page_len=10, weighting=None, **kwargs):
        try:
            searcher = self.get_searcher(index_name, weighting=weighting)
            query_parser = QueryParser(search_field, self.get_schema(index_name))
            query_obj = query_parser.parse(query)
            try:
                self.__logger.debug('searching documents in {0}: {1}'.format(index_name, query_obj))
                results_page = searcher.search_page(query_obj, page_num, pagelen=page_len, **kwargs)
            except Exception as ex:
                self.__logger.error('failed to search documents in {0}: {1}'.format(index_name, query_obj))
                raise ex
        except Exception as ex:
            self.__logger.error('failed to search documents in {0}'.format(index_name))
            raise ex

        return results_page

    def open_snapshot_file(self):
        try:
            f = open(self.__conf.fullDumpFile, mode='rb')
        except Exception as ex:
            raise ex

        return f
