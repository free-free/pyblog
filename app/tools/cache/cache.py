#-*- coding:utf-8 -*-
from cache_factory import CacheFactory
from tools.config import Config
class Cache(object):
	def __init__(self,driver=None,config=None)
		driver=driver or Config.cache.driver_name
		config=config or Config.cache.all
		assert isinstance(driver,str)
		assert isinstance(config,dict)
		self.__default_cache_driver=self._driver(driver,config)
		self.__current_cache_driver=self.__default_cache_driver
	def driver(self,driver,config):
		self.__current_cache_driver=self._driver(driver,config)
	def _driver(self,driver,config):
		return CacheFactory(driver,config)
	def put(self,key,value,expires=None):
		self.__current_cache_driver.put(key,value,expires)
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
	def update(self,key,value,expires=None)
		result=self.__current_cache_driver.update(key,value,expires)
		self.__current_cache_driver=self.__default_cache_driver
	def exists(self,key):
		result=self.__current_cache_driver.exists(key)
		self.__current_cache_driver=self.__default_cache_driver
		return result
	def delete(self,key):
		result=self.__current_cache_driver.delete(key)
		self.__current_cache_driver=self.__default_cache_driver
		return result
	
		

