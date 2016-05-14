#-*- coding:utf-8 -*-
import logging
logging.basicConfig(level=logging.ERROR)
from pyblog.storage.qiniu_storage import QiniuStorageAdapter
from pyblog.storage.storage_abstract import StorageAbstractAdapter

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
if __name__=='__main__':
	pass
