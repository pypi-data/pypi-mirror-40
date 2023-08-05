# -*- coding: utf-8 -*-

import os
import copy
import logging
from logging import config

from . import config_data

logger_sub_dirs = [
    'utils',
    'auth',
]

class AppLogger(object):
    logger_sub_dirs = []

    def __init__(self, app=None):
        self.app = None
        self._logger_dir = None

        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        self.app = app

        self.init_dirs()

        self._set_root_logger()

    def init_dirs(self):
        if not self.logger_dir:
            return

        for sub_dir in (*self.logger_sub_dirs, *logger_sub_dirs):
            sub_dir = os.path.join(self.logger_dir, sub_dir)
            if not os.path.exists(sub_dir):
                os.makedirs(sub_dir)

    @property
    def logger_dir(self):
        return self._logger_dir

    @property
    def config(self):
        return {}

    def _set_root_logger(self):
        config = self._get_config()
        configuration = self._merge_dict_config(config, self.config)
        logging.config.dictConfig(configuration)

    def _get_config(self):
        if self.logger_dir:
            handler_class = 'logging.handlers.TimedRotatingFileHandler'
            backup_count = 10
            when = 'midnight'
        else:
            handler_class = 'logging.StreamHandler'
            stream = 'ext://sys.stdout'

        handlers = copy.copy(config_data.handlers)
        logging_config = copy.copy(config_data.logging_config)

        if self.logger_dir:
            backup_count = 10
            when = 'midnight'

            handlers['utils_debug']['class'] = handler_class
            handlers['utils_debug']['filename'] = os.path.join(self.logger_dir, 'utils', 'debug.log')
            handlers['utils_debug']['backupCount'] = backup_count
            handlers['utils_debug']['when'] = when

            handlers['utils_warning']['class'] = handler_class
            handlers['utils_warning']['filename'] = os.path.join(self.logger_dir, 'utils', 'warning.log')
            handlers['utils_warning']['backupCount'] = backup_count
            handlers['utils_warning']['when'] = when

            handlers['auth_debug']['class'] = handler_class
            handlers['auth_debug']['filename'] = os.path.join(self.logger_dir, 'auth', 'debug.log')
            handlers['auth_debug']['backupCount'] = backup_count
            handlers['auth_debug']['when'] = when

            handlers['auth_warning']['class'] = handler_class
            handlers['auth_warning']['filename'] = os.path.join(self.logger_dir, 'auth', 'warning.log')
            handlers['auth_warning']['backupCount'] = backup_count
            handlers['auth_warning']['when'] = when
        else:
            stream = 'ext://sys.stdout'

            handlers['utils_debug']['stream'] = stream
            handlers['utils_warning']['stream'] = stream
            handlers['auth_debug']['stream'] = stream
            handlers['auth_warning']['stream'] = stream

        logging_config['handlers'] = handlers

        return logging_config

    def _merge_dict_config(self, overridden, overriding):
        if overriding is None or not isinstance(overriding, dict):
            overriding = {}

        formatters = copy.copy(overridden.get('formatters', {}))
        formatters.update(overriding.get('formatters', {}))

        handlers = copy.copy(overridden.get('handlers', {}))
        handlers.update(overriding.get('handlers', {}))

        loggers = copy.copy(overridden.get('loggers', {}))
        loggers.update(overriding.get('loggers', {}))

        configuration = {
            'version': 1,
            'disable_existing_loggers': False,
            'formatters': formatters,
            'handlers': handlers,
            'loggers': loggers,
        }

        return configuration
