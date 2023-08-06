import logging

from logging_config.components.formatter import LogstashJsonEncoder
from logging_config.constants import *


class DefaultComponents:
    """
    Contains methods to return default logging components
    """

    @staticmethod
    def get_filters():
        filters = {
            'debug_filter': {
                '()': 'logging_config.components.filters.LogLevelFilter',
                'level': logging.DEBUG
            },
            'info_filter': {
                '()': 'logging_config.components.filters.LogLevelFilter',
                'level': logging.INFO
            },
            'warn_filter': {
                '()': 'logging_config.components.filters.LogLevelFilter',
                'level': logging.WARN
            },
            'error_filter': {
                '()': 'logging_config.components.filters.LogLevelFilter',
                'level': logging.ERROR
            },
        }
        return filters

    @staticmethod
    def get_formatters():
        formatters = {
            'std_output': {
                'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            },
            'json_output': {
                '()': 'logstash_formatter.LogstashFormatterV1',
                'json_cls': LogstashJsonEncoder
            },
        }
        return formatters

    @staticmethod
    def get_handlers(log_root):
        handlers = dict(debug_handler=DefaultComponents.create_handler(log_root, DEFAULT_LOG_HANDLER_CLASS, 'DEBUG',
                                                                       DEBUG_LOG_FILE, ['debug_filter'], 'json_output'),

                        info_handler=DefaultComponents.create_handler(log_root, DEFAULT_LOG_HANDLER_CLASS, 'INFO',
                                                                      INFO_LOG_FILE, ['info_filter'], 'json_output'),

                        warn_handler=DefaultComponents.create_handler(log_root, DEFAULT_LOG_HANDLER_CLASS, 'WARN',
                                                                      WARN_LOG_FILE, ['warn_filter'], 'json_output'),

                        error_handler=DefaultComponents.create_handler(log_root, DEFAULT_LOG_HANDLER_CLASS, 'ERROR',
                                                                       ERROR_LOG_FILE, ['error_filter'], 'json_output'))
        return handlers

    @staticmethod
    def get_loggers():
        loggers = {
            '': DefaultComponents.create_logger(handlers=['debug_handler', 'info_handler', 'warn_handler',
                                                          'error_handler'],
                                                level='INFO')
        }
        return loggers

    @staticmethod
    def create_handler(log_root, handler_class, level, filename, filters, formatter):
        return {
            'class': handler_class,
            'level': level,
            'filters': filters,
            'formatter': formatter,
            'filename': log_root + '/' + filename
        }

    @staticmethod
    def create_logger(handlers, level, propagate=True):
        return {
            'handlers': handlers,
            'level': level,
            'propagate': propagate
        }
