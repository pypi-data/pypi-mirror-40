# -*- coding:utf-8 -*-
"""
    log Filters
"""

import logging


class LogLevelFilter(logging.Filter):
    """
        LogLevelFilter
    """
    def __init__(self, level):
        """
        :param level:
        """
        self.level = level
        super(LogLevelFilter, self).__init__('')

    def filter(self, record):
        """
        :param record:
        :return:
        """
        return record.levelno == self.level
