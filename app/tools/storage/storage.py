#-*- coding:utf-8 -*-

from tools.config import Config
from tools.storage.storage_factory import StorageDriverFactory
class Storage(object):
	def __init__(self,config=None):
		self.__config=config
		self.__disk={}
		self.__default_disk=self._get_storage_driver(Config.storage.disk_name,Config.storage.all)
		self.__current_disk=self.__default_disk
	def _get_storage_driver(self,driver,config):
		return StorageDriverFactory(driver,config)
	def disk(self,disk_name):
		if disk_name not in self.__disk:
			driver=Config.storage.disk(disk_name).driver
			all_config=Config.storage.disk(disk_name).all
			self.__disk[disk_name]=self._get_storage_driver(driver,all_config)
		self.__current_disk=self.__disk[disk_name]
		return self
	def move(self,src,dest):
		ret=self.__current_disk.move(src,dest)
		self.__current_disk=self.__default_disk
		return ret
	def rename(self,src_old,src_new):
		return self.move(src_old,src_new)
	def copy(self,src,dest):
		ret=self.__current_disk.copy(src,dest)
		self.__current_disk=self.__default_disk
		return ret
	def delete(self,file_name):
		ret=self.__current_disk.delete(file_name)
		self.__current_disk=self.__default_disk
		return ret
	def file_size(self,file_name):
		ret=self.__current_disk.file_size(file_name)
		self.__current_disk=self.__default_disk
		return ret
	def file_hash(self,file_name):
		ret=self.__current__disk.file_hash(file_name)
		self.__current_disk=self.__default_disk
		return ret
	def file_ctime(self,file_name):
		ret=self.__current_disk.file_create_time(file_name)
		self.__current_disk=self.__default_disk
		return ret
	def file_mime(self,file_name):
		ret=self.__current_disk.file_mime(file_name)
		self.__current_disk=self.__default_disk
		return ret
	def token(self,file_name,**kw):
		ret=self.__current_disk.token(file_name,**kw)
		self.__current_disk=self.__default_disk
		return ret
	def put(self,file_name,local_file,**kw):
		ret=self.__current_disk.put(file_name,local_file,**kw)
		self.__current_disk=self.__default_disk
		return ret
	def get(self,file_name,**kw):
		pass
	def get_url(self,file_name,**kw):
		ret=self.__current_disk.get_url(file_name,**kw)
		self.__current_disk=self.__default_disk
		return ret
if __name__=='__main__':
	pass



