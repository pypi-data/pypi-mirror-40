# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：    zlogger.py
   Author :       Zhang Fan
   date：         19/01/07
   Description :
-------------------------------------------------
"""
__author__ = 'Zhang Fan'

import os
import logging
from enum import Enum


class logger_level(Enum):
    notset = 'NOTSET'
    debug = 'DEBUG'
    info = 'INFO'
    warning = 'WARNING'
    warn = 'WARNING'
    error = 'ERROR'
    critical = 'CRITICAL'
    fatal = 'CRITICAL'


class _logger():
    _instance = None
    format = '%(asctime)s||%(name)s(%(process)d)||%(filename)s--%(module)s--%(funcName)s:%(lineno)d||%(levelname)s||%(message)s'

    def __init__(self, name, write_stream=True, write_file=False, file_dir='.', level=logger_level.debug,
                 interval=1, backupCount=2):
        '''
        构建日志对象
        :param name: 日志名
        :param write_stream: 是否输出日志到流(终端)
        :param write_file: 是否输出日志到文件
        :param file_dir: 日志文件的目录
        :param level: 日志等级
        :param interval: 间隔多少天重新创建一个日志文件
        :param backupCount: 保留历史日志文件数量
        '''
        self.name = name.lower()
        self.log_path = os.path.abspath(file_dir)
        self.pid = os.getpid()

        self.write_stream = write_stream
        self.write_file = write_file
        self.level = level
        self.interval = interval
        self.backupCount = backupCount

        self.level_getter = lambda x: eval("logging" + "." + x.upper())

        self.logger = logging.getLogger(self.name)
        self.logger.setLevel(self.level_getter(self.level.value))
        self._set_logger()
        self.logger.propagate = False  # 此处不设置，可能会打印2遍log

    def _set_logger(self):
        if self.write_stream:
            sh = self._get_stream_handler()
            self.logger.addHandler(sh)

        if self.write_file:
            fh = self._get_file_handler()
            self.logger.addHandler(fh)

    def _get_stream_handler(self):
        sh = logging.StreamHandler()
        sh.setLevel(self.level_getter(self.level.value))
        fmt = logging.Formatter(fmt=self.format)
        sh.setFormatter(fmt)
        return sh

    def _get_file_handler(self):
        filename = os.path.abspath(os.path.join(self.log_path, '{}_{}.log'.format(self.name, self.pid)))
        from random import randint
        filename += str(randint(0, 10000)) + '.log'

        from logging.handlers import TimedRotatingFileHandler
        fh = TimedRotatingFileHandler(filename, 'D', self.interval, backupCount=self.backupCount,
                                      encoding='utf-8')
        fh.setLevel(self.level_getter(self.level.value))
        fmt = logging.Formatter(fmt=self.format)
        fh.setFormatter(fmt)
        return fh


def logger(name, write_stream=True, write_file=False, file_dir='.', level=logger_level.debug,
           interval=1, backupCount=2):
    return _logger(name, write_stream, write_file, file_dir, level, interval, backupCount).logger


def logger_singleton(name, write_stream=True, write_file=False, file_dir='.', level=logger_level.debug,
                     interval=1, backupCount=2):
    if _logger._instance is None:
        _logger._instance = _logger(name, write_stream, write_file, file_dir, level, interval, backupCount).logger
    return _logger._instance
