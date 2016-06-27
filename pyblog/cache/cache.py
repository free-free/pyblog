#-*- coding:utf-8 -*-
from cache_factory import CacheFactory
from pyblog.config import Config


class Cache(object):

    def __init__(self, driver=None, config=None):
        driver = driver or Config.cache.driver_name
        config = config or Config.cache.all
        assert isinstance(driver, str)
        assert isinstance(config, dict)
        self.__default_cache_driver = self._driver(driver, config)
        self.__current_cache_driver = self.__default_cache_driver
        self.__resolved_drivers = dict()
        self.__factory = CacheFactory

    def driver(self, driver, config=None):
        if driver in self.__resolved_drivers:
            print("first instance after")
            return self.__resolved_drivers.get(driver)
        if not config:
            config = Config.cache.driver(driver).all
        self.__resolved_drivers[driver] = Cache(driver, config)
        print("first instance ")
        return self.__resolved_drivers[driver]

    def _driver(self, driver, config):
        return self.__factory(driver, config)

    def put(self, key, value, expires=0, key_prefix=""):
        return self.__current_cache_driver.put(key, value, expires, key_prefix)

    def get(self, key, key_prefix=""):
        return self.__current_cache_driver.get(key, key_prefix)

    def get_delete(self, key, key_prefix=""):
        return self.__current_cache_driver.get_delete(key, key_prefix)

    def increment(self, key, delta=1, key_prefix=""):
        return self.__current_cache_driver.increment(key, delta, key_prefix)

    def decrement(self, key, delta=1, key_prefix=""):
        return self.__current_cache_driver.decrement(key, delta, key_prefix)

    def update(self, key, value, expires=0, key_prefix=""):
        return self.__current_cache_driver.update(key, value, expires, key_prefix)

    def exists(self, key, key_prefix=""):
        return self.__current_cache_driver.exists(key, key_prefix)

    def delete(self, key, key_prefix=""):
        return self.__current_cache_driver.delete(key, key_prefix)


if __name__ == '__main__':
    pass
    '''
	#cache=Cache()
	#cache.put("user",{"name":"john","email":"19941222hb@gmail.com","age":21})
	#cache.put("user:id",[1,3,4,5,3,2,3,4,2,1,21])
	#cache.put("user:name","john")
	#print(cache.get_delete("user"))
	#print(cache.get_delete("user:id"))
	#print(cache.get_delete("user:name"))
	#cache.driver("memcache").put("user:1",{"name":"xxx"})
	#cache.driver("memcache").put("user:2",{"name":"yyy"})
	#cache.driver("memcache").put("user:3",{"name":"zzz"})
	#cache.driver("memcache").put("user:4",{"name":"jjj"})
	#print(cache.driver("memcache").get_delete("user:1"))
	#print(cache.driver("memcache").get_delete("user:2"))
	#print(cache.driver("memcache").get_delete("user:3"))
	#print(cache.driver("memcache").get_delete("user:4"))
	'''
