#-*- coding:utf-8 -*-
class CacheAbstractDriver:
	def __init__(self,*args,**kw):
		pass
	def put(self,key,value,expires=None,key_prefix=""):
		raise NotImplementedError
	def get(self,key,key_prefix=""):
		raise NotImplementedError
	def get_delete(self,key,key_prefix=""):
		raise NotImplementedError
	def delete(self,key,key_prefix=""):
		raise NotImplementedError
	def update(self,key,value,expires=None,key_prefix=""):
		raise NotImplementedError
	def exists(self,key,key_prefix=""):
		raise NotImplementedError
	def increment(self,key,num=None,key_prefix=""):
		raise NotImplementedError
	def decrement(self,key,num=None,key_prefix=""):
		raise NotImplementedError
