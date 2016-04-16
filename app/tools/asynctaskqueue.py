#-*- coding:utf-8 -*-
import logging
logging.basciConfig(level=logging.ERROR)
import asyncio
try:
	import aiomysql
except ImportError:
	logging.error("can't import 'aiomysql' module")

class ConfigError(StandardError):
	pass

class AsyncMysqlConnection(object):
	conn=dict()
	def __init__(self,host,port,user,password,db):
		assert isinstance(host,str)
		assert isinstance(port,int)
		assert isinstance(user,str)
		assert isinstance(password,str)
		assert isinstance(db,str)
		self._host=host
		self._port=port
		self._user=user
		self._password=password
		self._db=db
		self._loop
	@asyncio.coroutine
	def get_connection(self,loop,db=None):
		if not db:
			if self._db not self._conn:
				self._conn[self._db]=yield from aiomysql.connect(host=self._host,
								port=self._port,
								user=self._user,
								password=self._password,
								db=self._db
								loop=loop)
			return self._conn[self._db]
		else:
			if db not in self._conn:
				self._conn[self._db]=yield from aiomysql.connect(host=self._host,
									port=self._port,
									user=self._user,
									password=self._password,
									db=db,
									loop=loop)
			return self._conn[db]
class Queue(object):
	def __init__(self,config):
		self._config=config
	def enqueue(self,queue_name,value):
		pass
	def dequeue(self,queue_name):
		pass
	def __getattr__(self,key):
		if key.split('_',1)[1] in self._config:
			return self._config.get(key.split('_',1)[1])
		else:
			raise ConfigError("no '%s' config item"%key.split('_',1)[1])
	
		
