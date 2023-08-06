# Benchmarking Suite
# Copyright 2014-2017 Engineering Ingegneria Informatica S.p.A.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Developed in the ARTIST EU project (www.artist-project.eu) and in the
# CloudPerfect EU project (https://cloudperfect.eu/)
import logging

import datetime
import pytz
from pymongo import MongoClient
from benchsuite.core.model.storage import StorageConnector
from benchsuite.core.model.execution import ExecutionResult

logger = logging.getLogger(__name__)


class MongoDBStorageConnector(StorageConnector):

    def __init__(self):
        self.client = None
        self.db = None
        self.collection = None
        self.err_collection = None
        self.store_logs = False

    def save_execution_error(self, exec_error):
        r = self.err_collection.insert_one(exec_error.__dict__)
        logger.info('Execution error saved with with id=%s', r.inserted_id)

    def save_execution_result(self, execution_result: ExecutionResult):

        r = self.collection.insert_one(self.__create_record(execution_result))

        logger.info('New execution results stored with id=%s', r.inserted_id)



    def __create_record(self, execution_result: ExecutionResult):

        record = {
            'schema_ver': 2,
            'starttime': datetime.datetime.fromtimestamp(
                execution_result.start, tz=pytz.utc),
            'metrics': execution_result.metrics,
            'test': {
                'tool': execution_result.tool,
                'workload': execution_result.workload
            },
            'provider': execution_result.provider,
            'execution': {
                'environment': execution_result.exec_env
            }
        }

        # optinal fields
        if execution_result.properties:
            record['properties'] = execution_result.properties

        if execution_result.categories:
            record['test']['categories'] = execution_result.categories

        if execution_result.workload_description:
            record['test']['description'] = execution_result.workload_description

        if self.store_logs:
            record['execution']['logs'] = execution_result.logs

        self.__sanitize_record(record)

        return record

    def __sanitize_record(self, record):
        if 'properties' in record:
            newd = dict(record['properties'])
            for k,v in record['properties'].items():
                if '.' in k:
                    newd.pop(k)
                    newd[k.replace('.','_dot_')] = v
            record['properties'] = newd


    @staticmethod
    def load_from_config(config):

        # define some defaults
        if 'error_collection_name' not in config['Storage']:
            config['Storage']['error_collection_name'] = 'exec_errors'

        if 'store_logs' not in config['Storage']:
            config['Storage']['store_logs'] = "False"

        logger.debug('Loading %s', MongoDBStorageConnector.__module__ + "." + __class__.__name__)

        o = MongoDBStorageConnector()
        o.client = MongoClient(config['Storage']['connection_string'])
        o.db = o.client[config['Storage']['db_name']]
        o.collection = o.db[config['Storage']['collection_name']]
        o.err_collection = o.db[config['Storage']['error_collection_name']]
        if config['Storage']['store_logs'].lower() in ('true', 'yes', 'y', '1'):
            o.store_logs = True
        else:
            o.store_logs = False

        logger.info('MongoDBStorageConnector created for %s, db=%s, coll=%s', config['Storage']['connection_string'], config['Storage']['db_name'], config['Storage']['collection_name'])

        return o


