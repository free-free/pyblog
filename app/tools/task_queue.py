#-*- coding:utf-8 -*-
import logging
logging.basicConfig(level=logging.ERROR)
try:
	import redis
except ImportError:
	logging.error("can't import 'redis' module")
	exit()
try:
	import pymongo
	from pymongo import MongoClient
except ImportError:
	logging.error("can't import 'pymongo' module")
	exit()

class RedisQueue(object):
	_pool=None
	def __init__(self,config=None):
		if config:
			self._host=config.get('host','localhost')	
			self._port=config.get('port',6379)
			self._db=config.get('db',0)
		else:
			self._host='localhost'
			self._port=6379
			self._db=0
		if not type(self)._pool:
			type(self)._pool=redis.ConnectionPool(host=self._host,port=self._port,db=self._db)
		self._redis_conn=redis.Redis(connection_pool=type(self._pool))
		super(RedisQueue,self).__init__()
	def enqueue(self,queue_name,content):
		self._redis_conn.lpush(queue_name,content)
		return content
	def dequeue(self,queue_name):
		return self._redis_conn.rpop(queue_name)
class MongoQueue(object):
	def __init__(self,config=None):
		if config:
			self._host=config.get('host','localhost')
			self._port=config.get('port',27017)
			self._db=config.get('db','queue')
			self._collection=config.get('collection','queue_collection')
		else:
			self._host='localhost'
			self._port=27017
			self._db='queue'
			self._collection='queue_collection'
		self._client=MongoClient(self._host,self._port)
		self._mongo_conn=self._client[self._db][self._collection]
		super(MongoQueue,self).__init__()
	def enqueue(self,content,queue_name=None):
		if queue_name:
			mongo_conn=self._client[self._db][queue_name]
		
			

