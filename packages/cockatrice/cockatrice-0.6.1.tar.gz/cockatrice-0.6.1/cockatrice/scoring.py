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

import yaml
from whoosh.scoring import BM25F, MultiWeighting

from cockatrice.util.loader import get_instance


def get_weighting(class_name, **class_args):
    try:
        weighting = get_instance(class_name, **class_args)
    except Exception as ex:
        raise ex

    return weighting


def get_multi_weighting(weighting_yaml):
    try:
        __dict = yaml.safe_load(weighting_yaml)

        default_weighting = BM25F
        weighting_dict = {}

        for field_name in __dict['weighting'].keys():
            class_name = __dict['weighting'][field_name]['class']
            class_args = __dict['weighting'][field_name]['args'] if 'args' in __dict['weighting'][field_name] else {}
            instance = get_instance(class_name, **class_args)
            if field_name == 'default':
                default_weighting = instance
            else:
                weighting_dict[field_name] = instance

        weighting = MultiWeighting(default_weighting, **weighting_dict)
    except Exception as ex:
        raise ex

    return weighting
