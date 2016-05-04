#-*- coding:utf-8 -*-
import logging
logging.basicConfig(level=logging.ERROR)
from tools.storage.qiniu_storage import QiniuStorageAdapter


class StorageDriverFactory(object):
	def __new__(cls,*args,**kw):
		assert isinstance(args[0],str)
		assert isinstance(args[1],dict)
		cls.__driver=args[0]
		cls.__config=args[1]
		return eval("cls._get_%s_storage_driver(%s)"%(cls.__driver,cls.__config))
	@classmethod
	def _get_qiniu_storage_driver(cls,config):
		return QiniuStorageAdapter(config.get("bucket"),config.get("access_key"),config.get("secret_key"))




if __name__=='__main__':
	pass
	r'''
	print(type(StorageDriverFactory('qiniu',dict(bucket="static-pyblog-com",access_key="HUHIUHEDIUHIDUEHIUH",secret_key="hduiehiudei"))))
	'''
