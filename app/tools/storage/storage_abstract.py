#-*- coding:utf-8 -*-
import logging
logging.basicConfig(level=logging.ERROR)


class StorageAbstractAdapter(object):
	def __init__(self,*args,**kw):
		pass
	def move(self,src,dest):
		pass
	def copy(self,src,dest):
		pass
	def delete(self,src):
		pass
	def file_size(self,file_name):
		pass
	def file_hash(self,file_name):
		pass
	def file_info(self,file_name):
		pass
	def file_mime(self,file_name):
		pass
	def file_create_time(self,file_name):
		pass
	def upload(self,token,file_name,local_file):
		pass
	def upload_token(self,file_name,expire=3600,policy=None):
		pass
	def download_url(self,domain,file_name,expire=3600):
		pass
	
	

