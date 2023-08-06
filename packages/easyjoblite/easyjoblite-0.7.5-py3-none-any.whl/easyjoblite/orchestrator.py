# -*- coding: utf-8 -*-

import logging
import os
import signal
import subprocess
import time
import traceback
from multiprocessing import Process

from kombu import Connection
from kombu import Exchange
from kombu import Producer
from kombu import Queue

from easyjoblite import constants
from easyjoblite import state
from easyjoblite.configuration import Configuration
from easyjoblite.consumers.dead_letter_queue_consumer import DeadLetterQueueConsumer
from easyjoblite.consumers.retry_queue_consumer import RetryQueueConsumer
from easyjoblite.consumers.work_queue_consumer import WorkQueueConsumer
from easyjoblite.exception import EasyJobServiceNotStarted
from easyjoblite.job import EasyJob
from easyjoblite.utils import enqueue, is_main_thread
from easyjoblite.workers import worker_manager

logger = logging.getLogger(__name__)


class Orchestrator(object):
    """
    The central class to expose the core features of the library for usage.
    """

    def __init__(self, **kwargs):

        # Initialize varaibles
        self.consumer_creater_map = {
            constants.WORK_QUEUE: self.create_work_cunsumer,
            constants.RETRY_QUEUE: self.create_retry_queue_consumer,
            constants.DEAD_LETTER_QUEUE: self.create_dead_letter_queue_consumer
        }
        self._service_inited = False
        self._booking_exchange = None
        self._run_healthcheck = False
        self._is_master = False

        # Initialize config
        self._config = Configuration(**kwargs)

        # Add signal handler
        if is_main_thread():
            logger.info("Adding signal handler.")
            signal.signal(signal.SIGTERM, self.orchestrator_signal_term_handler)

    def validate_init(self):
        if not self._service_inited:
            raise EasyJobServiceNotStarted()

    def get_connection(self):
        self.validate_init()
        return self._conn

    def get_config(self):
        return self._config

    def get_exchange(self):
        return self._booking_exchange

    def update_consumer_pid(self, type, pid):
        service_state = state.ServiceState(self.get_config().pid_file_path)
        service_state.add_worker_pid(type, pid)

    def set_config(self, **kwargs):
        """
        set config values
        :param kwargs: contains the dict with all key values
        :return: 
        """
        self._config.set_config(**kwargs)

    def start_service(self, is_detached=False, run_health_check=True):
        """
        starts the service
        :return: 
        """
        # Setup the entities
        self.setup_entities()

        # create all consumers
        self.create_all_consumers(is_detached)

        # start health check
        if run_health_check:
            self._run_healthcheck = True
            self._is_master = True
            self.run_health_check()

    def create_all_consumers(self, is_detached=False):
        """
        creates all the consumes needed by the service
        :param is_detached: 
        :return: 
        """
        # create the workers
        for i in range(self._config.default_worker_count):
            self.create_consumer(constants.WORK_QUEUE, is_detached)
            time.sleep(2)

        # create the retry queue consumers
        for i in range(self._config.default_retry_consumer_count):
            self.create_consumer(constants.RETRY_QUEUE, is_detached)
            time.sleep(2)

        # create the dead letter consumers
        for i in range(self._config.default_dl_consumer_count):
            self.create_consumer(constants.DEAD_LETTER_QUEUE, is_detached)
            time.sleep(2)

    def setup_entities(self):
        """
        declare all required entities
        no advanced error handling yet (like error on declaration with altered properties etc)
        """
        # return if already inited
        if self._service_inited:
            return

        # setup exchange
        self._booking_exchange = Exchange(self._config.get_mq_config(constants.EXCHANGE),
                                          type='topic',
                                          durable=True)

        # setup durable queues
        self.work_queue = Queue(self._config.get_mq_config(constants.WORK_QUEUE),
                                exchange=self._booking_exchange,
                                routing_key=constants.WORK_QUEUE + ".#",
                                durable=True)

        self.retry_queue = Queue(self._config.get_mq_config(constants.RETRY_QUEUE),
                                 exchange=self._booking_exchange,
                                 routing_key=constants.RETRY_QUEUE + ".#",
                                 durable=True)

        self.dlq_queue = Queue(self._config.get_mq_config(constants.DEAD_LETTER_QUEUE),
                               exchange=self._booking_exchange,
                               routing_key=constants.DEAD_LETTER_QUEUE + ".#",
                               durable=True)

        # a buffer queue is needed by error-queue-consumer to temp-buffer msgs for processing
        # this is to handle retry loop which may cause between retry-queue and work-queue.
        # todo: Need to implement an alternive as this has a copy overhead
        #  which can be significant when the error queue is large
        self.buffer_queue = Queue(name=self._config.get_mq_config(constants.BUFFER_QUEUE),
                                  exchange=self._booking_exchange,
                                  routing_key='buffer.#',
                                  durable=True)

        # todo: do we need to make confirm_publish configurable?
        self._conn = Connection(self.get_config().rabbitmq_url,
                                transport_options={'confirm_publish': True},
                                heartbeat=self.get_config().rmq_config.heartbeat_interval)

        # declare all the exchanges and queues needed (declare, not overwrite existing)
        for entity in [self._booking_exchange, self.work_queue, self.retry_queue,
                       self.dlq_queue, self.buffer_queue]:
            entity.maybe_bind(self._conn)
            entity.declare()

        # setup producer to push to error and dlqs
        self._producer = Producer(channel=self._conn.channel(),
                                  exchange=self._booking_exchange)

        self._service_inited = True

    def create_consumer(self, type, is_detached=False):
        """
        create a worker for the queue
        :param type: type of worker
        :param is_detached: if true then will run as a seperate process else will run as a fork of the script.
        :return: 
        """
        if is_detached:
            self.create_consumer_detached(type)
        else:
            self.fork_consumer(type)

    def fork_consumer(self, type):
        """
        create a consumer by forking the current processes
        :param type: type of worker
        :return: none
        """
        p = Process(target=self.start_consumer, args=(type,))
        p.start()
        self.update_consumer_pid(type, p.pid)

    def create_consumer_detached(self, type):
        """
        create a consumer by calling the cli
        :param type: type of worker to be created
        :return: none
        """
        command_str = constants.BASE_COMMAND

        # Add command
        command_str += " start "

        # Add type
        command_str += str(type)

        # Add rabbitmq url
        command_str += " --url " + str(self.get_config().rabbitmq_url)

        # Add asyn timeout
        command_str += " --asyc_timeout " + str(self.get_config().async_timeout)

        # Add retry count
        command_str += " --max_retries " + str(self.get_config().max_retries)

        # Add retry queue sleep time
        command_str += " --eqc_sleep_duration " + str(self.get_config().eqc_sleep_duration)

        # Add import paths
        command_str += " --import_paths " + str(self.get_config().import_paths)

        # append log to log path
        command_str += " >" + self.get_config().workers_log_file_path

        # run in background
        command_str += "&"

        subprocess.Popen(command_str, shell=True)

    def stop_server(self, type=constants.STOP_TYPE_ALL):
        """
        Stop the server and kill all the workers
        :param type: the type of command
        :return: 
        """
        command_str = constants.BASE_COMMAND

        # Add stop command
        command_str += " stop "

        # Add type of command
        command_str += type

        # run in background
        command_str += " &"

        os.system(command_str)

    def start_consumer(self, worker_type):
        self.setup_entities()

        logging.basicConfig(filename=self.get_config().workers_log_file_path)
        logger = logging.getLogger(self.__class__.__name__)

        if worker_type not in self.consumer_creater_map:
            raise KeyError("Invalid consumer worker_type")

        try:
            self.consumer_creater_map[worker_type]()
        except Exception as e:
            traceback.print_exc()
            logger.error("Got an exception in the worker : {}".format(e.message))

        service_state = state.ServiceState(self.get_config().pid_file_path)
        service_state.remove_worker_pid(worker_type, os.getpid())
        logger.info("Quitting worker: {}".format(os.getpid()))
        exit(0)

    def create_work_cunsumer(self):
        self.validate_init()
        worker = WorkQueueConsumer(self)
        worker.consume_from_work_queue(self.work_queue)

    def create_retry_queue_consumer(self):
        self.validate_init()
        retry_consumer = RetryQueueConsumer(self)
        retry_consumer.consume_from_retry_queue(self.retry_queue, self.buffer_queue)

    def create_dead_letter_queue_consumer(self):
        self.validate_init()
        dead_letter_consumer = DeadLetterQueueConsumer(self)
        dead_letter_consumer.consume_from_dead_letter_queue(self.dlq_queue)

    def run_health_check(self):
        logger = logging.getLogger(self.__class__.__name__)
        logger.info("Initializing health check")

        # healthcheck job workers
        while self._run_healthcheck:
            logger.info("starting health check")
            self.match_required_worker(constants.WORK_QUEUE, self.get_config().default_worker_count)
            self.match_required_worker(constants.RETRY_QUEUE, self.get_config().default_retry_consumer_count)
            self.match_required_worker(constants.DEAD_LETTER_QUEUE, self.get_config().default_dl_consumer_count)

            logger.info("Done health check. will sleep for {} min.".format(self.get_config().health_check_interval))
            time.sleep(self.get_config().health_check_interval * 60)

        logger.info("Exiting health check")

    def match_required_worker(self, worker_type, required_count):
        """
        spawn missing worker
        :param worker_type: type of worker
        :param required_count: type of worker
        :return: 
        """
        logger = logging.getLogger(self.__class__.__name__)
        logger.info("doing healthcheck for {} workers for required {}".format(worker_type, required_count))
        service_state = state.ServiceState(self.get_config().pid_file_path)
        service_state.refresh_workers_pid(worker_type)

        worker_diff = required_count - len(service_state.get_pid_list(worker_type))

        if worker_diff > 0:
            logger.info("worker diff found for worker type: {} with diff {}"
                        .format(worker_type, worker_diff))
            for i in range(0, worker_diff):
                logger.info("starting consumer of type {}".format(worker_type))
                self.create_consumer(worker_type)

    def enqueue_job(self, api, type, tag=None, remote_call_type=None, data=None, api_request_headers=None,
                    content_type=None, notification_handler=None):
        """
        Enqueue a job to be processed.
        :param api: The api to be called when job is run
        :param type: The type of job (Remote/Local) when local then a python call is made and in remote an REST call is made.
        :param tag: a tag for the job to be run
        :param remote_call_type: is the call POST/GET/PUT
        :param data: a data payload to be passed along in the job
        :param api_request_headers: request headers to be passed along in a remote call
        :param content_type: content type to be used in remote call
        :param notification_handler: the api to be called when a job goes into dlq (type same as api)
        :return: A unique job id assigned to the job.
        """
        self.validate_init()

        # create the job
        job = EasyJob.create(api, type, tag=tag, remote_call_type=remote_call_type, data=data,
                             api_request_headers=api_request_headers,
                             content_type=content_type, notification_handler=notification_handler)

        # enqueue
        enqueue(self._producer, constants.WORK_QUEUE, job, data, self.get_config().rmq_config.retry,
                self.get_config().rmq_config.retry_policy)

        return job.id

    def orchestrator_signal_term_handler(self, signum, frame):
        """
        signal handler for the workers
        :param signum: 
        :param frame: 
        :return: 
        """
        logger = logging.getLogger(self.__class__.__name__)
        logger.warning("SIGTERM found so stopping worker with signum {0}".format(signum))
        self._run_healthcheck = False
        if self._is_master:
            worker_manager.stop_all_workers(constants.STOP_TYPE_ALL)
