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
try:
	import MySQLdb
except ImportError:
	logging.error("can't import 'MySQLdb' module")
	exit()
class DBConnection(object):
	def __init__(self):
		pass
	def __get__(self,obj,ownerclass):
		pass
	def __set__(self,obj,value):
		pass
	def __del__(self):
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
		if not self._check_connection_pool:
			self._create_connection_pool(obj._host,obj._port,obj._db)
		if not self._check_connection:
			return self._create_connection()
		return type(self)._connection
class MongoConnection(DBConnection):
	_client=None
	_connection=None
	def __init__(self):
		pass
	def _create_client(self,host,port):
		type(self)._client=MongoClient(host=host,port=port)
		return type(self)._client
	def _create_connection(self,db):
		type(self)._connection=type(self)._client[str(db)]
		return type(self)._connection
	@property
	def _check_client(self):
		if not type(self)._client:
			return False
		return True
	@property
	def _check_connection(self):
		if not type(self)._connection:
			return False
		return True
	def __get__(self,obj,ownclass):
		if not self._check_client:
			self._create_client(obj._host,obj._port)
		if not self._check_connection:
			return self._create_connection(obj._db)
		return type(self)._connection
class MysqlConnection(DBConnection):
	_connection=None
	def __init__(self):
		pass
	def _create_connection(self,host,port,db,user,password):
		type(self)._connection=MySQLdb.connect(host=host,port=port,db=db,user=user,passwd=password,cursorclass=MySQL.cursors.DictCursor)
		return type(self)._connection
	@property
	def _check_connection(self):
		if not type(self)._connection:
			return False
		return True
	def __get__(self,obj,ownclass):
		if not self._check_connection:
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
			return self._config.get(key.split('_',1)[1])
		else:
			raise AttributeError("%s has no such attirbute"%type(self))
class RedisQueue(Queue):
	_redis_conn=RedisConnection()
	def __init__(self,config=None):
		if not config:	
			config=dict()
			config['host']='localhost'
			config['port']=6379
			config['db']=0
		super(RedisQueue,self).__init__(config)
	def enqueue(self,queue_name,content):
		self._redis_conn.lpush(queue_name,content)
		return content
	def dequeue(self,queue_name):
		return self._redis_conn.rpop(queue_name)
class MongoQueue(Queue):
	_mongo_conn=MongoConnection()
	def __init__(self,config=None):
		if not config:
			config=dict()
			config['host']='localhost'
			config['port']=27017
			config['db']='queue'
		super(MongoQueue,self).__init__(config)
	def enqueue(self,queue_name,content):
		pass
	def dequeue(self,queue_name):
		pass
class MysqlQueue(Queue):
	_mysql_conn=MysqlConnection()
	def __init__(self,config=None):
		if not config:
			config=dict()
			config['port']=3306
			config['host']='localhost'
			config['db']='queue'
			config['user']='root'
			config['password']='xxxx'
		super(MysqlQueue,self).__init__(config)
	def enqueue(self,queue_name,content):
		cursor=self._mysql_conn.cursor()
		cursor.execute("insert into `%s`(`content`,`enqueue_at`) values(%s,%s)"%(queue_name,content,content,str(int(time.time()))))
		cursor.close()
		self._mysql_conn.commit()
		return content
	def dequeue(self,queue_name):
		cursor=self._mysql_conn.cursor()
		ret=cursor.findone()
		cursor.close()
		return ret
if __name__=='__main__':
	rqueue=RedisQueue()
	rqueue.dequeue("email")
	#rqueue.enqueue("email",'sent to 19941222hb@gmail.com')		
	#rqueue.enqueue("email",'sent to 18281573692@gmail.com')		
	#rqueue.enqueue("email",'sent to xxxx@gmail.com')		
	#rqueue.enqueue("email",'sent to yyyyy@gmail.com')		
