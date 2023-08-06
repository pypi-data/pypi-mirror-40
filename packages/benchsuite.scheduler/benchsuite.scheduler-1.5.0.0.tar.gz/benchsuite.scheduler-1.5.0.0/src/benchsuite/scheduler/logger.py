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

from apscheduler.events import EVENT_JOB_EXECUTED, EVENT_JOB_ERROR, \
    EVENT_JOB_MISSED, EVENT_JOB_ADDED, EVENT_JOB_REMOVED, EVENT_JOB_MODIFIED
from pymongo import MongoClient

from benchsuite.scheduler.jobs.meta import print_scheduled_jobs_info
from benchsuite.scheduler.synchronizer import JOB_ID_PREFIX, \
    BENCHMARKING_JOBSTORE

logger = logging.getLogger(__name__)

MONGO_SCHEMA_VER = 1

class JobExecutionLogger(object):
    """
    provides methods to log the execution of jobs in the console and in a
    MongoDB collection
    """

    _client = None

    _log_success_execution = None
    _log_error_execution = None
    _log_missed_execution = None


    def __init__(self, db_host, db_name, db_collection,
                 log_success_execution=True,
                 log_error_execution=True,
                 log_missed_execution=True):

        self._client = MongoClient(db_host)
        self._db_name = db_name
        self._db_collection = db_collection
        self._log_success_execution = log_success_execution
        self._log_error_execution = log_error_execution
        self._log_missed_execution = log_missed_execution

    def apscheduler_listener(self, evt):

        if not hasattr(evt, 'jobstore') or evt.jobstore != BENCHMARKING_JOBSTORE:
            return

        if evt.code == EVENT_JOB_EXECUTED:
            logger.info('[LOG] Job successfully executed')
            if self._log_success_execution:
                self.__add_entry('OK', evt)

        elif evt.code == EVENT_JOB_ERROR:
            logger.info('[LOG] Job ERROR')
            if self._log_error_execution:
                self.__add_entry('ERROR', evt)

        elif evt.code == EVENT_JOB_MISSED:
            logger.info('[LOG] Job MISSED')
            if self._log_missed_execution:
                self.__add_entry('MISSSED', evt)

        elif evt.code == EVENT_JOB_ADDED or \
            evt.code == EVENT_JOB_REMOVED or \
            evt.code == EVENT_JOB_MODIFIED:
                logger.info('Job list modified. Printing list')
                from benchsuite.scheduler.bsscheduler import get_bsscheduler
                print_scheduled_jobs_info(get_bsscheduler())

        else:
            logger.debug('Received event code %s that is not managed', evt.code)


    def _extract_exception_info(self, exception):

        if not exception:
            return {}

        starting_log = 'Exiting due to fatal error:'

        res = {'error': str(exception),
               'error_code': exception.status_code if hasattr(exception, 'status_code') else None,
               'error_log': None,
               'error_traceback': None}

        if hasattr(exception, 'log'):
            res['error_log'] = exception.log
            start = exception.log.find(starting_log) + len(starting_log)
            error_end = exception.log.find('\n', start)
            res['error'] = exception.log[start+1:error_end]
            res['error_traceback'] = exception.log[error_end+1:]

        return res


    def __add_entry(self, status, evt):
        obj = {
            'status': status,
            'time': evt.scheduled_run_time,
            'ap_job_id': evt.job_id,
            'schema_ver': MONGO_SCHEMA_VER,
        }

        if evt.job_id.startswith(JOB_ID_PREFIX):
            obj['schedule_id'] = evt.job_id[len(JOB_ID_PREFIX):]

        # add error info
        if status == 'ERROR':
            obj.update(self._extract_exception_info(evt.exception))

            # keep this for retrocompatibility
            obj['exception'] = obj['error']

            if hasattr(evt.exception, 'container'):

                # the container dict contains a "Labels" dict. However, keys of
                # the latter container may have "." because they are the name of
                # the labels (e.g. "com.docker.swarm.node.id"). So we sanitize
                # the names before storing

                new_labels = {}
                for k, v in evt.exception.container['Config']['Labels'].items():
                    new_labels[k.replace('.','_dot_')] = v
                evt.exception.container['Config']['Labels'] = new_labels

                obj['container'] = evt.exception.container

            obj['docker_exception'] = evt.traceback

        self._client[self._db_name][self._db_collection].insert_one(obj)
