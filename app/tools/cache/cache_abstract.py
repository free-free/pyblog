#-*- coding:utf-8 -*-
class CacheAbstractDriver(object):
	def __init__(self,*args,**kw):
		pass
	def put(self,key,value,expires=None,key_prefix=""):
		pass
	def get(self,key,key_prefix=""):
		pass
	def get_delete(self,key,key_prefix=""):
		pass
	def delete(self,key,key_prefix=""):
		pass
	def update(self,key,content,expires=None,key_prefix=""):
		pass
	def exists(self,key,key_prefix=""):
		pass
	def increment(self,key,num=None,key_prefix=""):
		pass
	def decrement(self,key,num=None,key_prefix=""):
		pass
