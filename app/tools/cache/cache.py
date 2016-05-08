#-*- coding:utf-8 -*-
from cache_factory import CacheFactory
from tools.config import Config
class Cache(object):
	def __init__(self,driver=None,config=None):
		driver=driver or Config.cache.driver_name
		config=config or Config.cache.all
		assert isinstance(driver,str)
		assert isinstance(config,dict)
		self.__default_cache_driver=self._driver(driver,config)
		self.__current_cache_driver=self.__default_cache_driver
	def driver(self,driver,config=None):
		if not config:
			config=Config.cache.driver(driver).all
		self.__current_cache_driver=self._driver(driver,config)
		return self
	def _driver(self,driver,config):
		return CacheFactory(driver,config)
	def put(self,key,value,expires=None):
		if expires:
			self.__current_cache_driver.put(key,value,expires)
		else:
			self.__current_cache_driver.put(key,value)
		self.__current_cache_driver=self.__default_cache_driver
	def get(self,key):
		result=self.__current_cache_driver.get(key)
		self.__current_cache_driver=self.__default_cache_driver
		return result
	def get_delete(self,key):
		result=self.__current_cache_driver.get_delete(key)
		self.__current_cache_driver=self.__default_cache_driver
		return result
	def increment(self,key,delta=1):
		result=self.__current_cache_driver.increment(key,delta)
		self.__current_cache_driver=self.__default_cache_driver
		return result
	def decrement(self,key,delta=1):
		result=self.__current_cache_driver.decrement(key,delta)
		self.__current_cache_driver=self.__default_cache_driver
		return result
	def update(self,key,value,expires=None):
		if expires:
			result=self.__current_cache_driver.update(key,value,expires)
		else:
			result=self.__current_cache_driver.update(key,value)
		self.__current_cache_driver=self.__default_cache_driver
	def exists(self,key):
		result=self.__current_cache_driver.exists(key)
		self.__current_cache_driver=self.__default_cache_driver
		return result
	def delete(self,key):
		result=self.__current_cache_driver.delete(key)
		self.__current_cache_driver=self.__default_cache_driver
		return result
	
		
if __name__=='__main__':
	pass
	#cache=Cache()
	#cache.driver("memcache").put("user:1",{"name":"xxx"})
	#print(cache.driver("memcache").get_delete("user:1"))
	
