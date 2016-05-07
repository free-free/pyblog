#-*- coding:utf-8 -*-
import logging
logging.basicConfig(level=logging.ERROR)
from cache_abstract import CacheAbstractDriver
try:
	import redis
except ImportError:
	logging.error("Can't import 'redis' module")
	exit(-1)


class RedisClient(object):
	def __init__(self,**kwargs):
		self.__host=kwargs.get('host')
		self.__port=kwargs.get('port')
		self.__db=kwargs.get("db")
		assert isinstance(self.__host,str)
		assert isinstance(self.__port,int)
		assert isinstance(self.__db,int) and 0<=self.__db<16
		self._connection=redis.StrictRedis(self.__host,self.__port,self.__db)
class RedisCache(CacheAbstractDriver,RedisClient):
	def __init__(self,cache_db,**kwargs):
		kwargs['db']=cache_db
		RedisClient.__init__(self,**kwargs)
	def __str__(self):
		return str(self._connection)
	def __repr__(self):
		return str(self._connection)



if __name__=='__main__':
	print(RedisCache(1,host='localhost',port=6379))

	
		
		
