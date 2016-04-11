#-*- coding:utf-8 -*-
import logging
logging.basicConfig(level=logging.ERROR)
try:
	import redis
except ImportError:
	logging.error("can't import 'redis' module")
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
	def enqueue(self,queue_name,content):
		self._redis_conn.lpush(queue_name,content)
		return content
	def dequeue(self,queue_name):
		return self._redis_conn.rpop(queue_name)
	

