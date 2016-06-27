#-*- coding:utf-8 -*-
class CacheAbstractDriver:

    def __init__(self, *args, **kw):
        pass

    def put(self, key, value, expires, key_prefix):
        r"""
            @put a value to cache system

            @parameters:
                key :must be 'str'  type or 'dict ' type
                        when 'key' is 'dict' type,value must be None value
                value:list,tuple,dict,None,one of them
                expires:must be 'int' type,units is seconds
                key_prefix: 'str' type
        """
        raise NotImplementedError

    def get(self, key, key_prefix):
        r"""
            @get a cache value from cache system
        """
        raise NotImplementedError

    def get_delete(self, key, key_prefix):
        r"""
            @get and delete a cache value from cache system
        """
        raise NotImplementedError

    def delete(self, key, key_prefix):
        r"""
            @delete a cache value from cache system
        """
        raise NotImplementedError

    def update(self, key, value, expires, key_prefix):
        r"""
            @update a cache value to cache system
        """
        raise NotImplementedError

    def exists(self, key, key_prefix):
        r"""
           @check a cache value whether existen
        """
        raise NotImplementedError

    def increment(self, key, delta, key_prefix):
        r"""
           @increment a cahce value
        """
        raise NotImplementedError

    def decrement(self, key, delta, key_prefix):
        r"""
           @decrement a cache value
        """
        raise NotImplementedError
