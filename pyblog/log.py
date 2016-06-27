#!/usr/bin/env python3

from datetime import datetime
import os
import functools


class staticproperty(object):

    def __init__(self, f_get, f_set=None, f_del=None):
        self._f_get = f_get
        self._f_set = f_set
        self._f_del = f_del

    def __get__(self, obj, ownclass):
        return self._f_get(ownclass)

    def __set__(self, obj, value):
        self._f_set(type(obj), value)

    def setter(self, f_set):
        def wrapper(*args, **kw):
            f_set(*args, **kw)
        self._f_set = wrapper


class Log(object):
    _logPath = os.path.abspath(os.path.join(
        os.path.dirname(__file__), '../../log'))
    _logName = 'pyblog' + str(datetime.date(datetime.now())) + '.log'
    _logFormat = """ [%s]  level:%s ==> %s \r\n"""
    __slots__ = tuple()

    def __init__(self):
        pass

    @classmethod
    def info(cls, info):
        with open(os.path.join(cls._logPath, cls._logName), 'a+') as f:
            f.write(cls._logFormat % (datetime.now(), 'INFO', info))

    @classmethod
    def warning(cls, info):
        with open(os.path.join(cls._logPath, cls._logName), 'a+') as f:
            f.write(cls._logFormat % (datetime.now(), 'WARNING', info))

    @classmethod
    def error(cls, info):
        with open(os.path.join(cls._logPath, cls._logName), 'a+') as f:
            f.write(cls._logFormat % (datetime.now(), 'ERROR', info))

    @classmethod
    def get_logpath(cls):
        return os.path.join(cls._logPath, cls._logName)

    @classmethod
    def set_logPath(cls, path):
        cls._logPath = path

    @classmethod
    def set_logformat(cls, logformat):
        cls._logFormat = logformat

    @classmethod
    def get_logformat(cls):
        return cls._logFormat

    @staticproperty
    def log_format(cls):
        return cls._logFormat

    @staticproperty
    def log_path(cls):
        print("getter")
        return cls._logPath
if __name__ == '__main__':
    r'''
    #sql='select * from user'.upper()
    #Log.error(sql)
    #Log.warning(sql)
    #Log.info(sql)
    '''
