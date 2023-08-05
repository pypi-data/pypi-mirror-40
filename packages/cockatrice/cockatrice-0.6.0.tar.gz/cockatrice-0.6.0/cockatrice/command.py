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

import os

from pysyncobj.poller import createPoller
from pysyncobj.tcp_connection import TcpConnection
from pysyncobj.encryptor import getEncryptor

import cockatrice
from cockatrice.util.resolver import get_ipv4


class Executor:
    def __init__(self, cmd, args=None, bind_addr=cockatrice.DEFAULT_BIND_ADDR, password=None, timeout=1):
        try:
            self.__result = None

            self.__request = [cmd]
            if args is not None:
                self.__request.extend(args)

            host, port = bind_addr.split(":", 1)

            self.__host = get_ipv4(host)
            self.__port = int(port)
            self.__password = password
            self.__poller = createPoller('auto')
            self.__connection = TcpConnection(self.__poller, onMessageReceived=self.__on_message_received,
                                              onConnected=self.__on_connected, onDisconnected=self.__on_disconnected,
                                              socket=None, timeout=10.0, sendBufferSize=2 ** 13, recvBufferSize=2 ** 13)
            if self.__password is not None:
                self.__connection.encryptor = getEncryptor(self.__password)
            self.__is_connected = self.__connection.connect(self.__host, self.__port)
            while self.__is_connected:
                self.__poller.poll(timeout)
        except Exception as ex:
            raise ex

    def __on_message_received(self, message):
        if self.__connection.encryptor and not self.__connection.sendRandKey:
            self.__connection.sendRandKey = message
            self.__connection.send(self.__request)
            return

        self.__result = message
        self.__connection.disconnect()

    def __on_connected(self):
        if self.__connection.encryptor:
            self.__connection.recvRandKey = os.urandom(32)
            self.__connection.send(self.__connection.recvRandKey)
            return

        self.__connection.send(self.__request)

    def __on_disconnected(self):
        self.__is_connected = False

    def get_result(self):
        return self.__result


def execute(cmd, args=None, bind_addr='127.0.0.1:7070', password=None, timeout=1):
    try:
        response = Executor(cmd, args=args, bind_addr=bind_addr, password=password, timeout=timeout).get_result()
    except Exception as ex:
        raise ex

    return response


def get_status(bind_addr='127.0.0.1:7070', password=None, timeout=1):
    return execute('status', args=None, bind_addr=bind_addr, password=password, timeout=timeout)


def add_node(node_name, bind_addr='127.0.0.1:7070', password=None, timeout=1):
    return execute('add', args=[node_name], bind_addr=bind_addr, password=password, timeout=timeout)


def delete_node(node_name, bind_addr='127.0.0.1:7070', password=None, timeout=1):
    return execute('remove', args=[node_name], bind_addr=bind_addr, password=password, timeout=timeout)


def get_snapshot(bind_addr='127.0.0.1:7070', password=None, timeout=1):
    return execute('get_snapshot', args=None, bind_addr=bind_addr, password=password, timeout=timeout)
