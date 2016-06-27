#-*- coding:utf-8 -*-
import logging
logging.basicConfig(level=logging.ERROR)
from cache_abstract import CacheAbstractDriver
import json
import six
try:
    import memcache
except ImportError:
    logging.error("Can't import 'memcache' module")
    exit(-1)


class MemcacheCacheClient(object):

    def __init__(self, servers, *args, **kw):
        self.__connection = memcache.Client(servers, *args, **kw)

    def set(self, key, val=None, expires=0, key_prefix="", min_compress_len=0):
        if not val:
            if isinstance(key, dict):
                return self.__connection.set_multi(key, expires, key_prefix, min_compress_len)
        else:
            if isinstance(val, dict):
                val = json.dumps(val)
            elif isinstance(val, (tuple, list, set)):
                val = list(val)
                val = map(lambda x: str(x), val)
                val = ']'.join(val)
            else:
                val = val
            return self.__connection.set(key_prefix + key, val, expires, min_compress_len)

    def get(self, key, key_prefix=""):
        if isinstance(key, six.string_types):
            values = self.__connection.get(key_prefix + key)
            if not values:
                return None
            new_values = ""
            try:
                new_values = json.loads(values)
            except Exception:
                new_values = values
            if not isinstance(new_values, dict):
                new_values = new_values.split("]")
                if len(new_values) == 1:
                    return new_values[0]
            return new_values
        elif isinstance(key, (tuple, list)):
            return self.__connection.get_multi(list(key), key_prefix)
        else:
            pass

    def delete(self, key, key_prefix=""):
        if isinstance(key, six.string_types):
            self.__connection.delete(key_prefix + key)
        elif isinstance(key, (tuple, list)):
            return self.__connection.delete_multi(list(key), key_prefix)
        else:
            pass

    def inc(self, key, delta=1, key_prefix=""):
        if isinstance(key, six.string_types):
            key = key_prefix + key
            return self.__connection.incr(key, int(delta))
        elif isinstance(key, (tuple, list)):
            returns = []
            for k in key:
                returns.append(self.__connection.incr(
                    key_prefix + k, int(delta)))
            return returns
        elif isinstance(key, dict):
            r'''
                    key={"key1":"delta1","key2":"delta2".....}
            '''
            returns = []
            for k, de in key.items():
                returns.append(self.__connection.incr(key_prefix + k, int(de)))
            return returns
        else:
            pass

    def dec(self, key, delta=1, key_prefix=""):
        if isinstance(key, six.string_types):
            return self.__connection.decr(key_prefix + key, delta)
        elif isinstance(key, (list, tuple)):
            returns = []
            for k in key:
                returns.append(self.__connection.decr(
                    key_prefix + k, int(delta)))
            return returns
        elif isinstance(key, dict):
            returns = []
            for k, de in key.items():
                returns.append(self.__connection.decr(key_prefix + k, int(de)))
            return returns
        else:
            pass


class MemcacheCache(CacheAbstractDriver):

    def __init__(self, host, port, *args, **kw):
        isinstance(host, str)
        isinstance(port, (str, int))
        self.__client = MemcacheCacheClient(
            [str(host) + ':' + str(port)], *args, **kw)

    def put(self, key, value=None, expires=0, key_prefix=""):
        return self.__client.set(key, value, expires, key_prefix)

    def get(self, key, key_prefix=""):
        return self.__client.get(key, key_prefix)

    def get_delete(self, key, key_prefix=""):
        values = self.__client.get(key, key_prefix)
        self.delete(key, key_prefix)
        return values

    def increment(self, key, delta=1, key_prefix=""):
        return self.__client.inc(key, delta, key_prefix)

    def decrement(self, key, delta=1, key_prefix=""):
        return self.__client.dec(key, delta, key_prefix)

    def delete(self, key, key_prefix=""):
        return self.__client.delete(key, key_prefix)

    def update(self, key, value=None, expires=0, key_prefix=""):
        return self.put(key, value, expires, key_prefix)

    def exists(self, key, key_prefix):
        return self.get(key, key_prefix) or False


if __name__ == '__main__':
    pass
    r'''
	#mc=MemcacheCache('127.0.0.1',11211)
	#mc.put("user:1",{"name":"huangbiao","age":21})
	#print(mc.get("user:1"))
	#print(mc.get_delete("user:1"))

	#mc.put({"name":"john","age":21})
	#print(mc.get(['name','age']))
	#print(mc.get_delete(['name','age']))	
	
	#mc.put("user:1",[323,23,43,43,24])
	#print(mc.get_delete("user:1"))
	#print(mc.get("user:1"))
	
	#mc.put("name",'huangbia',key_prefix="student:")
	#print(mc.get("name",key_prefix="student:"))
	#print(mc.get_delete("name",key_prefix="student:"))
	#print(mc.get("name",key_prefix="student:"))
	#mc.put({"age":21,"year":2016})
	#print(mc.increment(["age","year"]))
	#print(mc.decrement(["age","year"]))
	#print(mc.increment({"age":21,"year":20}))
	#print(mc.decrement({"age":21,"year":20}))
	#print(mc.get(["age","year"]))	
	'''
