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
class MemcacheCacheClient(object):
	def __init__(self,servers,*args,**kw):
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
			self.__connection.delete(key)
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
	def __init__(self,host,port):
		self.__client=MemcacheCacheClient([str(host)+':'+str(port)])
	def put(self,key,value=None,expires=0,key_prefix="",min_compress_len=0):
		return self.__client.set(key,value,expires,key_prefix,min_compress_len)
	def get(self,key,key_prefix=""):
		return self.__client.get(key,key_prefix)
	def get_delete(self,key,key_prefix=""):
		values=self.__client.get(key,key_prefix)
		self.delete(key,key_prefix)
		return values
	def increment(self,key,delta=1):
		return self.__client.inc(key,delta)
	def decrement(self,key,delta=1):
		return self.__client.dec(key,delta)
	def delete(self,key,key_prefix=""):
		return self.__client.delete(key,key_prefix)
	def update(self,key,value=None,expires=0,key_prefix="",min_compress_len=0):
		return self.put(key,value,expires,key_prefix,min_compress_len)
	def exists(self,key,key_prefix):
		return self.get(key,key_prefix) or False
	
	
	
if __name__=='__main__':
	mc=MemcacheCache('127.0.0.1',11211)
	#mc.put({"name":"huangbiao","age":21})
	#print(mc.get(['name','age']))
	
	mc.put("user:1",{"name":"huangbiao","age":21})
	print(mc.get("user:1"))
	#mc.put("name",'huangbia')
	#print(mc.get("name"))
	#print(mc.get_delete("name"))
	#print(mc.get("name"))
	
