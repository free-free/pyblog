#-*- coding:utf-8 -*-
import logging
logging.basicConfig(level=logging.ERROR)
from cache_abstract import CacheAbstractDriver
try:
	import redis
except ImportError:
	logging.error("Can't import 'redis' module")
	exit(-1)
try:
	import aioredis
except ImportError:
	logging.error("Can't import 'aioredis' module")
	exit(-1)
class AsyncRedisCacheClient(object):
	def __init__(self,host,port,db,*args,*kwargs):
		assert isinstance(host,str)
		assert isinstance(port,int)
		assert isinstance(db,int) and 0<=self.__db<16
		self.__host=host
		self.__port=port
		self.__db=db
		self.__connection=None
		self.__key_type_map={
				"1":"string",
				"2":"hash",
				"3":"list"
		}
		self.__key_type_hash="_key_type"
	@asyncio.coroutine
	def get_connection(self,loop=None):
		self.__connection=yield from aioredis.create_redis((self.__host,self.__port),db=self.__db,loop=loop)
		return self.__connection
	@asyncio.coroutine
	def set(self,key,value=None,expires,key_prefix):
		if not self.__connection:
			yield from self.get_connection()
		if not value and isinstance(key,dict):
			pipe=self.__connection.pipeline()
			for k,item in keys.items():
				pipe.hset(self.__key_type_hash,key_prefix+k,1)
				pipe.set(key_prefix+k,item)
				if expires>0:
					pipe.expire(key_prefix+k,expires)
			return (yield from pipe.execute())
		else:
			key=key_prefix+key
			if isinstance(value,str):
				pipe=self.__connection.pipeline()
				pipe.hset(self.__key_type_hash,key,1)
				pipe.set(key,value)
				if expires>0:
					pipe.expire(key,expires)
				return (yield from pipe.execute())
			elif isinstance(value,dict):
				pipe=self.__connection.pipeline()
				pipe.hset(self.__key_type_hash,key,2)
				pipe.hmset(key,value)
				if expires>0:
					pipe.expire(key,expires)
				return (yield from pipe.execute())
			elif isinstance(value,(list,tuple)):
				pipe=self.__connection.pipeline()
				pipe.hset(self.__key_type_hash,key,3)
				value=list(value)
				pipe.lpush(key,*value)
				if expires>0:
					pipe.expire(key,expires)		
				return (yield from pipe.execute())
	@asyncio.coroutine		
	def get(self,key,key_prefix):
		if not self.__connection
			yield from self.get_connection()
		key_type=yield from self.exists(key,key_prefix)
		key=key_prefix+key
		if key_type=="string":
			return (yield from self.__connection.get(key)) or ""
		elif key_type=="hash":
			return (yield from self.__connection.hgetall(key)) or {}
		elif key_type=="list":
			return (yield from self.__connection.lrange(key,0,-1)) or []
		else:
			return None
	@asyncio.coroutine
	def exists(self,key,key_prefix):
		key=key_prefix+key
		if not self.__connection:
			yield from self.get_connection()	
		key_type=self.__connection.hget(self.__key_type_hash,key)
		if key_type:
			return self.__key_type_map.get(key_type.decode("utf-8"))
		return None
	@asyncio.coroutine
	def delete_key(self,key,key_prefix):
		if not self.__connection:
			yield from self.get_connection()
		key=key_prefix+key
		return (yield from self.__connection.hdel(self.__key_type_hash,key))			
	@asyncio.coroutine
	def delete(self,key,key_prefix):
		key_type=yield from self.exists(key,key_prefix)
		result=""
		if key_type=="string":
			result=yield from self.__connection.delete(key_prefix+key)
		elif key_type=="hash":
			result=yield from self.__connection.hdel(key,*self._connection.hkeys(key_prefix+key))
		elif key_type=="list":
			length=yield from self.__connection.llen(key_prefix+key)
			if length:
				result=yield from self.__connection.ltrim(key_prefix+key,length+1,length+1)
		else:
			result=None
		yield from self.delete_key(key,key_prefix)
		return result
	
class RedisCacheClient(object):
	def __init__(self,host,port,db,*args,**kwargs):
		assert isinstance(host,str)
		assert isinstance(port,int)
		assert isinstance(db,int) and 0<=self.__db<16
		self.__host=host
		self.__port=port
		self.__db=db 
		self._connection=redis.StrictRedis(self.__host,self.__port,self.__db)
		self.__key_type_map={
			"1":"string",
			"2":"hash",
			"3":"list"
		}
		self.__key_type_hash="_key_type"
	def set(self,key,value=None,expires,key_prefix):
		if not value and isinstance(key,dict):
			pipe=self._connection.pipeline()
			for k,item in key.items():
				pipe.hset(self.__key_type_hash,key_prefix+k,1)
				pipe.set(key_prefix+k,item)
				if expires>0:
					pipe.expire(key_prefix+k,expires)
			return pipe.execute()
		else:	
			key=key_prefix+key
			if isinstance(value,str):
				pipe=self._connection.pipeline()
				pipe.hset(self.__key_type_hash,key,1)
				pipe.set(key,value)
				if expires>0:
					pipe.expire(key,expires)
				return pipe.execute()
			elif isinstance(value,dict):
				pipe=self._connection.pipeline()
				pipe.hset(self.__key_type_hash,key,2)
				pipe.hmset(key,value)
				if expires>0:
					pipe.expire(key,expires)
				return pipe.execute()
			elif isinstance(value,(list,tuple)):
				pipe=self._connection.pipeline()
				pipe.hset(self.__key_type_hash,key,3)
				pipe.lpush(key,*value)
				if expires>0:
					pipe.expire(key,expires)
				return pipe.execute()
	def get(self,key,key_prefix):
		key_type=self.exists(key,key_prefix)
		key=key_prefix+key
		if key_type=="string":
			return self._connection.get(key) or ""
		elif key_type=="hash":
			return self._connection.hgetall(key) or {}
		elif key_type=="list":
			return self._connection.lrange(key,0,-1) or []
		else:
			return None
	def delete(self,key,key_prefix):
		key_type=self.exists(key,key_prefix)
		result=""
		if key_type=="string":
			result=self._connection.delete(key_prefix+key)
		elif key_type=="hash":
			result=self._connection.hdel(key,*self._connection.hkeys(key_prefix+key))
		elif key_type=="list":
			length=self._connection.llen(key_prefix+key)
			if length:
				result=self._connection.ltrim(key_prefix+key,length+1,length+1)
		else:
			result=None
		self.delete_key(key,key_prefix)
		return result
	def inc(self,key,delta,key_prefix):
		key_type=self.exists(key,key_prefix)
		key=key_prefix+key
		if key_type=="string":
			return self._connection.incrby(key,delta)
		else:
			raise TypeError("can't  increment  '%s'"%key)
	def dec(self,key,delta,key_prefix):
		key_type=self.exists(key,key_prefix)
		key=key_prefix+key
		if key_type=="string":
			return self._connection.incrby(key,delta)
		else:
			raise TypeError("can't decrement '%s'"%key)
	def exists(self,key,key_prefix):	
		key=key_prefix+key
		key_type=self._connection.hget(self.__key_type_hash,key)
		if key_type:
			return self.__key_type_map.get(key_type.decode("utf-8"))
		return None
	def delete_key(self,key,key_prefix):
		return self._connection.hdel(self.__key_type_hash,key_prefix+key)
class RedisCache(CacheAbstractDriver):
	def __init__(self,host,port,cache_db,*args,**kwargs):
		self.__client=RedisCacheClient(host,port,cache_db,*args,**kwargs)
	def __str__(self):
		return str(self.__client)
	def __repr__(self):
		return str(self.__client)
	def put(self,key,value,expires=0,key_prefix=""):
		self.__client.set(key,value,expires,key_prefix)
	def delete(self,key,key_prefix=""):
		return self.__client.delete(key,key_prefix)
	def get(self,key,key_prefix=""):
		return self.__client.get(key,key_prefix)
	def get_delete(self,key,key_prefix=""):
		re=self.__client.get(key,key_prefix)
		self.__client.delete(key,key_prefix)
		return re
	def exists(self,key,key_prefix=""):
		return self.__client.exists(key,key_prefix)
	def increment(self,key,delta=1,key_prefix=""):
		return self.__client.inc(key,delta,key_prefix)
	def decrement(self,key,delta=1,key_prefix=""):
		return self.__client.dec(key,delta,key_prefix)
	def update(self,key,value,expires=0,key_prefix=""):
		return self.__client.set(key,value,expires,key_prefix)
	
	



if __name__=='__main__':
	pass
	r'''
	#re=RedisCache('localhost',6379,1)
	#re.put("1","hello",key_prefix="user:name:")
	#re.put("2",[21,32,32,121,42],key_prefix="user:list:")
	#re.put("3",{"name":"huangbiao","age":22,"email":"19941222hb@gmail.com"},key_prefix="user:info:")
	#print(re.get_delete("3",key_prefix="user:info:"))
	#print(re.get_delete("2",key_prefix="user:list:"))
	#print(re.get_delete("1",key_prefix="user:name:"))
	#print(re.get("user:3"))
	'''


	
		
		
