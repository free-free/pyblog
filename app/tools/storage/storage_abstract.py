#-*- coding:utf-8 -*-
import logging
logging.basicConfig(level=logging.ERROR)


class StorageAbstractAdapter:
	r'''
		A abatract interface class ,that provides a common interface to access it for different third party service

	'''
	def __init__(self,*args,**kw):
		r'''
			The init parameter is unique for different storage service
		'''
		pass
	def move(self,src,dest):
		r'''
			the mean of the parameter may represent different means
		'''
		raise NotImplementedError
	def copy(self,src,dest):
		raise NotImplementedError
	def delete(self,src):
		raise NotImplementedError
	def file_size(self,file_name):
		raise NotImplementedError
	def file_hash(self,file_name):
		raise NotImplementedError
	def file_info(self,file_name):
		raise NotImplementedError
	def file_mime(self,file_name):
		raise NotImplementedError
	def file_create_time(self,file_name):
		raise NotImplementedError
	def put(self,token,file_name,**kw):
		r'''
			**kw is different for different implmentation
		''' 
		raise NotImplementedError
	def token(self,file_name,**kw):
		raise NotImplementedError
	def get(self,file_name,**kw):
		raise NotImplementedError
	def get_url(self,file_name,**kw):
		raise NotImplementedError
	

