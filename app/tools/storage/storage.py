#-*- coding:utf-8 -*-

from tools.config import Config
from tools.storage.qiniu_storage import QiniuStorageAdapter
class Storage(object):
	def __init__(self,config=None):
		self.__config=config
		self.__disk={}
		self.__specific_disk=None
		self.__default_disk=self.disk(Config.storage.disk_name)
	def _get_qiniu_storage_driver(self,config):
		return QiniuStorageAdapter(config.get("bucket"),config.get("access_key"),config.get("secret_key"))
	def _get_file_storage_driver(self,config):
		pass
	def disk(self,disk_name):
		if disk_name not in self.__disk:
			driver=Config.storage.disk(disk_name).driver
			all_config=Config.storage.disk(disk_name).all
			self.__disk[disk_name]=eval("self._get_%s_storage_driver(%s)"%(driver,all_config))
		self.__specific_disk=self.__disk[disk_name]
		return self
	def move(self,src,dest):
		if self.__specific_disk:
			ret=self.__specific_disk.move(src,dest)
			self.__specific_disk=None
			return ret
		return self.__default_disk.move(src,dest)
	def copy(self,src,dest):
		if self.__specific_disk:
			ret=self.__specific_disk.copy(src,dest)
			self.__specific_disk=None
			return ret
		return self.__default_disk.copy(src,dest)
	def delete(self,file_name):
		if self.__specific_disk:
			ret=self.__specific_disk.delete(file_name)
			self.__specific_disk=None
			return ret
		return self.__default_disk.delete(file_name)
	
			
		
		
if __name__=='__main__':
	print(Storage())



	
