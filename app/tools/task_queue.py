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
class DBConnection(object):
	def __init__(self):
		pass
	def __get__(self,obj,ownerclass):
		pass
	def __set__(self,obj,value):
		pass
	def __del__(self,obj):
		pass
class RedisConnection(DBConnection):
	_connection=None
	_connection_pool=None
	def __init__(self):
		pass
	def _create_connection_pool(self,host,port,db):
		type(self)._connection_pool=redis.ConnectionPool(host=host,port=port,db=db)
		return type(self)._connection_pool
	def _create_connection(self):
		type(self)._connection=redis.StrictRedis(connection_pool=type(self)._connection_pool)
		return type(self)._connection
	@property
	def _check_connection_pool(self):
		if not type(self)._connection_pool:
			return False
		return True
	@property
	def _check_connection(self):
		if not type(self)._connection:
			return False
		return True
	def __get__(self,obj,ownclass):
		if self._check_connection_pool:
			self._create_connection_pool(obj._host,obj._port,obj._db)
		if self._check_connection:
			return self._create_connection()
		return type(self)._connection
			
class Queue(object):
	def __init__(self,config):
		self._config=config
	def enqueue(self,queue_name,content):
		pass
	def dequeue(self,queue_name):
		pass
	def __getattr__(self,key):
		if key.split('_',1)[1] in self._config:
			return self._config.get(key)
		else:
			raise AttributeError("%s has no such attirbute"%type(self))
class RedisQueue(Queue):
	def __init__(self,config=None):
		if not config:
			config['host']='localhost'
			config['port']=6379
			config['db']=0
		self._redis_conn=RedisConnnection()
		super(RedisQueue,self).__init__(config)
	def enqueue(self,queue_name,content):
		self._redis_conn.lpush(queue_name,content)
		return content
	def dequeue(self,queue_name):
		return self._redis_conn.rpop(queue_name)
class MongoQueue(Queue):
	_mongo_conn=None
	_client=None
	def __init__(self,config=None):
		if not config:
			config['host']='localhost'
			config['port']=27017
			config['db']='queue'
			config['collection']='default_queue'
		self._client=MongoClient(self._host,self._port)
		self._mongo_conn=self._client[self._db][self._collection]
		super(MongoQueue,self).__init__(config)
	def _get_connection(self):
		if not type(self)._client:
			type(self)._client=MongoClient(self._host,self._port)
		if not type(self)._mongo_conn:
			pass
	def enqueue(self,content,queue_name=None):
		if queue_name:
			mongo_conn=self._client[self._db][queue_name]
		
