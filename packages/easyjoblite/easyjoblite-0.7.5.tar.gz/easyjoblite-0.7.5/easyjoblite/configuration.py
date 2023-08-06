# -*- coding: utf-8 -*-

import logging
import traceback
import yaml

from easyjoblite import constants
from easyjoblite.utils import update_import_paths


class RabbitMQConfig(object):
    def __init__(self, heartbeat_interval, prefetch_count, retry, retry_policy):
        self.heartbeat_interval = heartbeat_interval
        self.prefetch_count = prefetch_count
        self.retry = retry
        self.retry_policy = retry_policy

    def __str__(self):
        return str(self.__dict__)


class Configuration(object):
    """
    used to configure the service
    """

    def __init__(self, **kwargs):
        """
        :param app_id: the application specific unique name.
        :param rabbitmq_url: where it the rabbitmq server running?
        :param max_retries: max retries before a message moves to DLQ
        :param async_timeout: wait these many seconds before we timeout async reqs
        :param eqc_sleep_duration: how long (in mins) should error-queue-consumer sleep between bursts
        :param max_worker_count: max ammount of job workers
        :param default_worker_count: default about of job worker to be spawned
        :param default_retry_consumer_count: default amount of retry consumer to be spawned
        :param default_dl_consumer_count: default amount of dead letter consumer to be spawned
        :param import_paths: the paths for looking to import modules for local run
        :param pid_file_path: the path to store the pid files of all the workers
        :param workers_log_file_path: the path to log from workers
        :param dead_message_log_file: the path to dump the dead letter messages without a event handler
        :param config_file: the path to store configuration
        :param health_check_interval: the health check interval when run in orchestrator mode
        :param rmq_config: the advanced config for rabbitmq
        """

        # first initialize everything with defaults
        self.load_with_defaults()

        # then check if config file is there if yes then load from it
        if 'config_file' in kwargs:
            self.config_file = kwargs['config_file']

        self.load_from_file(self.config_file)

        # now load any run time config change done
        self.set_config(**kwargs)

    def load_with_defaults(self):
        self.app_id = constants.DEFAULT_APP_ID
        self.rabbitmq_url = constants.DEFAULT_RMQ_URL
        self.max_retries = constants.DEFAULT_MAX_JOB_RETRIES
        self.async_timeout = constants.DEFAULT_ASYNC_TIMEOUT
        self.eqc_sleep_duration = constants.DEFAULT_ERROR_Q_CON_SLEEP_DURATION
        self.max_worker_count = constants.DEFAULT_MAX_WORKER_COUNT
        self.default_worker_count = constants.DEFAULT_WORKER_COUNT
        self.default_retry_consumer_count = constants.DEFAULT_RETRY_CONSUMER_COUNT
        self.default_dl_consumer_count = constants.DEFAULT_DLQ_CONSUMER_COUNT
        self.import_paths = constants.DEFAULT_IMPORT_PATHS
        self.pid_file_path = constants.DEFAULT_PID_FILE_LOCATION
        self.workers_log_file_path = constants.DEFAULT_LOG_FILE_PATH
        self.dead_message_log_file = constants.DEFAULT_DL_LOG_FILE
        self.config_file = constants.DEFAULT_CONFIG_FILE
        self.health_check_interval = constants.DEFAULT_HEALTH_CHECK_INTERVAL
        self.rmq_config = RabbitMQConfig(heartbeat_interval=constants.DEFAULT_RMQ_HEARTBEAT_INTERVAL,
                                         prefetch_count=constants.DEFAULT_RMQ_PREFETCH_COUNT,
                                         retry=constants.DEFAULT_RMQ_SHOULD_RETRY,
                                         retry_policy=constants.DEFAULT_RMQ_RETRY_POLICY)
        update_import_paths(self.import_paths)

    def set_config(self, **kwargs):
        """
        set config values
        :param kwargs: contains the dict with all key values
        :return: 
        """
        if 'app_id' in kwargs:
            self.app_id = kwargs['app_id']

        if 'rabbitmq_url' in kwargs:
            self.rabbitmq_url = kwargs['rabbitmq_url']

        if 'async_timeout' in kwargs:
            self.async_timeout = kwargs['async_timeout']

        if 'max_retries' in kwargs:
            self.max_retries = kwargs['max_retries']

        if 'eqc_sleep_duration' in kwargs:
            self.eqc_sleep_duration = kwargs['eqc_sleep_duration']

        if 'import_paths' in kwargs:
            self.import_paths = kwargs['import_paths']
            update_import_paths(self.import_paths)

        if 'max_worker_count' in kwargs:
            self.max_worker_count = kwargs['max_worker_count']

        if 'default_worker_count' in kwargs:
            self.default_worker_count = kwargs['default_worker_count']

        if 'default_retry_consumer_count' in kwargs:
            self.default_retry_consumer_count = kwargs['default_retry_consumer_count']

        if 'default_dl_consumer_count' in kwargs:
            self.default_dl_consumer_count = kwargs['default_dl_consumer_count']

        if 'workers_log_file_path' in kwargs:
            self.workers_log_file_path = kwargs['workers_log_file_path']

        if 'dead_message_log_file' in kwargs:
            self.dead_message_log_file = kwargs['dead_message_log_file']

        if 'config_file' in kwargs:
            self.config_file = kwargs['config_file']

        if 'health_check_interval' in kwargs:
            self.health_check_interval = kwargs['health_check_interval']

        if 'rmq_config' in kwargs:
            self.rmq_config = RabbitMQConfig(**kwargs['rmq_config'])

    def load_from_file(self, file_path):
        logger = logging.getLogger(self.__class__.__name__)
        try:
            with open(file_path, 'r') as stream:
                loaded_config = yaml.load(stream)
                self.set_config(**loaded_config)
        except Exception as e:
            traceback.print_exc()
            logger.error("Unable to load config file: {0} with exception {1}".format(str(file_path), e))
            self.load_with_defaults()
            self.dump_to_file(file_path)

    def dump_to_file(self, file_path):
        logger = logging.getLogger(self.__class__.__name__)
        conf_dict = {
            "app_id": self.app_id,
            "rabbitmq_url": self.rabbitmq_url,
            "max_retries": self.max_retries,
            "async_timeout": self.async_timeout,
            "eqc_sleep_duration": self.eqc_sleep_duration,
            "max_worker_count": self.max_worker_count,
            "default_worker_count": self.default_worker_count,
            "default_retry_consumer_count": self.default_retry_consumer_count,
            "default_dl_consumer_count": self.default_dl_consumer_count,
            "import_paths": self.import_paths,
            "pid_file_path": self.pid_file_path,
            "workers_log_file_path": self.workers_log_file_path,
            "dead_message_log_file": self.dead_message_log_file,
            "health_check_interval": self.health_check_interval,
            "rmq_config": self.rmq_config
        }

        try:
            config_file = open(file_path, "w")
            yaml.safe_dump(conf_dict, config_file, default_flow_style=False)
            config_file.close()
        except Exception as e:
            traceback.print_exc()
            logger.error("Unable to dump config file: {0} with exception {1}".format(str(file_path), e))

    def get_mq_config(self, conf_type):
        """
        return the rabbitmq config type
        :param conf_type: type like EXCHANGE, WORK_QUEUE, RETRY_QUEUE etc
        :return: 
        """
        return self.app_id + constants.rabbit_mq_prefix[conf_type]
