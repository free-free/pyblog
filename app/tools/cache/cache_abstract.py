#-*- coding:utf-8 -*-
class CacheAbstractDriver(object):
	def __init__(self,*args,**kw):
		pass
	def put(self,key,content,expires=None):
		pass
	def get(self,key):
		pass
	def get_delete(self,key):
		pass
	def delete(self,key):
		pass
	def update(self,key,content,expires=None):
		pass
	def exists(self,key):
		pass
