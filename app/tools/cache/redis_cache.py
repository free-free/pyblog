#-*- coding:utf-8 -*-
import logging
logging.basicConfig(level=logging.ERROR)
from cache_abstract import CacheAbstractDriver
try:
	import redis
except ImportError:
	logging.error("Can't import 'redis' module")
	exit(-1)


class RedisCacheClient(object):
	def __init__(self,**kwargs):
		self.__host=kwargs.get('host')
		self.__port=kwargs.get('port')
		self.__db=kwargs.get("db")
		assert isinstance(self.__host,str)
		assert isinstance(self.__port,int)
		assert isinstance(self.__db,int) and 0<=self.__db<16
		self._connection=redis.StrictRedis(self.__host,self.__port,self.__db)
		self.__key_type_map={
			"1":"string",
			"2":"hash",
			"3":"list"
		}
		self.__key_type_hash="_key_type"
	def add(self,key,content,expires):
		if isinstance(content,str):
			pipe=self._connection.pipeline()
			pipe.hset(self.__key_type_hash,key,1)
			pipe.set(key,content)
			if expires:
				pipe.expire(key,expires)
			pipe.execute()
		elif isinstance(content,dict):
			pipe=self._connection.pipeline()
			pipe.hset(self.__key_type_hash,key,2)
			pipe.hmset(key,content)
			if expires:
				pipe.expire(key,expires)
			pipe.execute()
		elif isinstance(content,(list,tuple)):
			pipe=self._connection.pipeline()
			pipe.hset(self.__key_type_hash,key,3)
			pipe.lpush(key,*content)
			if expires:
				pipe.expire(key,expires)
			pipe.execute()
	def get(self,key):
		key_type=self.exists(key)
		if key_type=="string":
			return self._connection.get(key) or ""
		elif key_type=="hash":
			return self._connection.hgetall(key) or {}
		elif key_type=="list":
			return self._connection.lrange(key,0,-1) or []
		else:
			return None
	def delete(self,key):
		key_type=self.exists(key)
		result=""
		if key_type=="string":
			result=self._connection.delete(key)
		elif key_type=="hash":
			result=self._connection.hdel(key,*self._connection.hkeys(key))
		elif key_type=="list":
			length=self._connection.llen(key)
			if length:
				result=self._connection.ltrim(key,length+1,length+1)
		else:
			result=None
		self.delete_key(key)
		return result
	def inc(self,key,num=None):
		num=num or 1
		key_type=self.exists(key)
		if key_type=="string":
			return self._connection.incrby(key,num)
		else:
			raise TypeError("can't  increment  '%s'"%key)
	def dec(self,key,num=None):
		num=num or 1
		key_type=self.exists(key)
		if key_type=="string":
			return self._connection.incrby(key,num)
		else:
			raise TypeError("can't decrement '%s'"%key)
	def exists(self,key):	
		key_type=self._connection.hget(self.__key_type_hash,key)
		if key_type:
			return self.__key_type_map.get(key_type.decode("utf-8"))
		return None
	def delete_key(self,key):
		return self._connection.hdel(self.__key_type_hash,key)
class RedisCache(CacheAbstractDriver):
	def __init__(self,cache_db,**kwargs):
		kwargs['db']=cache_db
		self.__client=RedisCacheClient(**kwargs)
	def __str__(self):
		return str(self.__client)
	def __repr__(self):
		return str(self.__client)
	def put(self,key,content,expires=None):
		self.__client.add(key,content,expires)
	def delete(self,key):
		return self.__client.delete(key)
	def get(self,key):
		return self.__client.get(key)
	def get_delete(self,key):
		re=self.__client.get(key)
		self.__client.delete(key)
		return re
	def exists(self,key):
		return self.__client.exists(key)
	def increment(self,key,num=None):
		return self.__client.inc(key,num)
	def decrement(self,key,num):
		return self.__client.dec(key,num)
	def update(self,key,expires):
		return self.__client.add(key,content,expires)
	
	



if __name__=='__main__':
	pass
	#re=RedisCache(1,host='localhost',port=6379)
	#re.put("user:1",list([12,32,3,23,23,2,32]))
	#re.delete("user:1")
	#print(re.get("user:1"))
	


	
		
		
