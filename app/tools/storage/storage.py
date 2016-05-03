#-*- coding:utf-8 -*-

from tools.config import Config
from tools.storage.qiniu_storage import QiniuStorageAdapter
class Storage(object):
	__slots__=('__bucket','__adapter','__config')
	def __init__(self,config=None):
		self.__config=config
		self.__adapter={}
	def get_qiniu_storage_adapter(self,config):
		if 'qiniu' not in self.__adapter:
			self.__adapater['qiniu']=QiniuStorageAdapater(config.get("bucket"),config.get("access_key"),config.get("secket_key"))
		return self.__adapter['qiniu']
	
