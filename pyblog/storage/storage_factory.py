#-*- coding:utf-8 -*-
import logging
logging.basicConfig(level=logging.ERROR)
from pyblog.storage.qiniu_storage import QiniuStorageAdapter
from pyblog.storage.storage_abstract import StorageAbstractAdapter
from collections import deque



class NoStorageDriverError(Exception):
	pass

class StorageDriverFactory(object):
	__drivers={'qiniu':QiniuStorageAdapter}
	def __new__(cls,*args,**kw):
		assert isinstance(args[0],str)
		assert isinstance(args[1],dict)
		cls.__driver=args[0]
		cls.__config=args[1]
		return cls._resolve_storage_driver(cls.__driver,cls.__config)
	@classmethod
	def register(self,driver_name,driver_class):
		assert isinstance(driver_name,str)
		assert isinstance(driver_class,StorageAbstractAdapter),"driver class extends StorageAbstractAdapter"
		cls.__drivers[driver_name]=driver_class
	@classmethod
	def _resolve_storage_driver(cls,driver_name,config):
		if driver_name in cls.__drivers:
			return cls.__drivers[driver_name](config)
		return None

class StorageCacheFactory(object):
	def __init__(self,config,min_cache=2,max_cache=4):
		assert isinstance(config,dict)
		assert isinstance(min_cache,int)
		assert isinstance(max_cache,int)
		self.__config=config
		self.__min_cache=min_cache
		self.__max_cache=max_cache
		self.__cache_size=0
		self.__storage_cache=deque()
		self.__driver_name=self.__config.get("driver").lower()
		if not hasattr(self,'get_%s_storage'%self.__driver_name):
			raise NoStorageDriverError(self.__driver_name)
		for i in range(0,self.__min_cache):
			self.__storage_cache.append(getattr(self,'get_%s_storage'%self.__driver_name)(self.__config))	
			self.__cache_size+=1
	def get_qiniu_storage(self,config):
		return QiniuStorageAdapter(config)
	def get_storage(self):
		return self._get_storage()
	def _get_storage(self):
		self._check_cache()
		instance=self.__storage_cache.popleft()
		self.__cache_size-=1
		return instance
	def _check_cache(self):
		if self.__cache_size<self.__min_cache:
			cache_size=self.__cache_size
			for i in range(0,(self.__max_cache-cache_size)//2):
				self.__storage_cache.append(getattr(self,'get_%s_storage'%self.__driver_name)(self.__config))
				self.__cache_size+=1
	def _add_to_cache(self,storage_instance):
		if not isinstance(storage_instance,StorageAbstractAdapter):
			return False
		if self.__cache_size>=self.__max_cache:
			return False
		self.__storage_cache.append(storage_instance)
		self.__cache_size+=1
		return True
	def cache(self,storage_instance):
		return self._add_to_cache(storage_instance)
		
if __name__=='__main__':
	pass
