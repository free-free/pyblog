#-*- coding:utf-8 -*-
import logging
logging.basicConfig(level=logging.ERROR)
from cache_abstract import CacheAbstractDriver
import json
import six
try:
	import memcache
except ImportError:
	logging.error("Can't import 'memcache' module")
	exit(-1)
class MemCacheCacheClient(object):
	def __init__(self,servers,args*,**kw):
		self.__connection=memcache.Client(servers,*args,**kw)
	def set(self,key,val=None,expires=0,key_prefix="",min_compress_len=0):
		if not val:
			if isinstance(key,dict):
				return self.__connection.set_multi(key,expires,key_prefix,min_compress_len)
		else:
			if isinstance(val,dict):
				val=json.dumps(val)
			elif isinstance(val,(tuple,list,set)):
				val=val.join(":")
			else:
				val=val
			return self.__connection.set(key,val,expires,min_compress_len)
	def get(self,key,key_prefix=""):
		if isinstance(key,six.string_types):
			return self.__connection.get(key)
		elif isinstance(key,(tuple,list)):
			return self.__connection.get_multi(list(key),key_prefix)
		else:
			pass
	def delete(self,key,key_prefix=""):
		if isinstance(key,six.string_types):
			return self.__connection.delete(key)
		elif isinstance(key,(tuple,list)):
			return self.__connection.delete_multi(list(key),key_prefix)
		else:
			pass
	def inc(self,key,delta=1):
		if isinstance(key,six.string_types):
			return self.__connection.incr(key,delta)
		elif isinstance(key,(tuple,list)):
			returns=[]
			for k in key:
				returns.append(self.__connection.incr(k,delta))
			return returns
		elif isinstance(key,dict):
			r'''
				key={"key1":"delta1","key2":"delta2".....}
			'''
			returns=[]
			for k,de in key.items():
				returns.append(self.__connection.incr(k,de))
			return returns
		else:
			pass
	def dec(self,key,delta=1):
		if isinstance(key,six.string_types):
			return self.__connection.decr(key,delta)
		elif isinstance(key,(list,tuple)):
			returns=[]
			for k in key:
				returns.append(self.__connection.decr(k,delta))
			return returns
		elif isinstance(key,dict):
			returns=[]	
			for k,de in key.items():
				returns.append(self.__connection.decr(k,de))
			return returns
		else:
			pass
		
class MemcacheCache(CacheAbstractDriver):
	def __init__(self,servers):
		assert isinstance(servers,list)
		self.__client=memcache.Client(servers)
	
