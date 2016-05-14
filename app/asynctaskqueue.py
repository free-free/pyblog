#-*- coding:utf-8 -*-
import logging
logging.basicConfig(level=logging.ERROR)
import asyncio
from tools.taskqueue import QueuePayloadJsonEncapsulator
from tools.config import Config
try:
	import aiomysql
except ImportError:
	logging.error("can't import 'aiomysql' module")
	exit(-1)
try:
	import aioredis
except ImportError:
	logging.error("can't import 'aioredis' module")
	exit(-1)

class ConfigError(Exception):
	pass
class AsyncRedisConnection(object):
	def __init__(self,host,port,loop=None):
		super(AsyncRedisConnection,self).__init__()
		assert isinstance(host,str)
		assert isinstance(port,int)
		self._host=host
		self._port=port
		self._loop=loop
		self._connection=None
	@asyncio.coroutine
	def get_connection(self,loop=None):
		if loop:
			self._loop=loop
		if self._loop:
			self._connection=yield from aioredis.create_redis((self._host,self._port),loop=self._loop)
		else:
			self._connection=yield from aioredis.create_redis((self._host,self._port))
		return self._connection
	@asyncio.coroutine
	def close(self):
		if self._connection:
			self._connection.close()
			yield from self._connection.wait_closed()
class AsyncMysqlConnection(object):
	_db_list=tuple()
	_table_list=tuple()
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
	@asyncio.coroutine
	def get_connection(self,loop,db=None):
		self._conn=yield from aiomysql.connect(host=self._host,
							port=self._port,
							user=self._user,
							password=self._password,
							loop=loop)
		yield from self._get_db_list()
		if not self._check_db(self._db):
			yield from self._create_db(self._db)
		yield from self._conn.select_db(self._db)
		return self._conn
	def _check_db(self,db_name):
		if db_name in self._db_list:
			return True
		return False
	@asyncio.coroutine
	def _get_db_list(self):
		cursor=yield from self._conn.cursor()
		yield from cursor.execute('show databases')
		dbs=yield from cursor.fetchall()
		yield from cursor.close()
		db_list=list()
		for db in dbs:
			db_list.append(db[0])
		self._db_list=tuple(db_list)
		return self._db_list
	@asyncio.coroutine
	def _create_db(self,db_name):
		yield from self._conn.begin()
		cursor=yield from self._conn.cursor()
		try:
			yield from cursor.execute("create database %s character set utf8"%db_name)
		except Exception:
			yield from self._conn.rollback()
		finally:
			yield from self._conn.commit()
			yield from cursor.close()
	@asyncio.coroutine
	def close(self):
		if self._conn:
			self._conn.close()	
class AsyncQueue(object):
	def __init__(self,config):
		self._config=config
	@asyncio.coroutine
	def enqueue(self,queue_name,payload):
		pass
	@asyncio.coroutine
	def dequeue(self,queue_name):
		pass
	def __getattr__(self,key):
		if key.split('_',1)[1] in self._config:
			return self._config.get(key.split('_',1)[1])
		else:
			raise ConfigError("no '%s' config item"%key.split('_',1)[1])
class AsyncRedisQueue(AsyncQueue):
	def __init__(self,config,loop=None,connection=AsyncRedisConnection):
		assert isinstance(config,dict)
		super(AsyncRedisQueue,self).__init__(config)
		self._connection_instance=connection(self._host,self._port,loop)
		self._connection=None
	@asyncio.coroutine
	def enqueue(self,queue_name,payload):
		if not self._connection:
			self._connection=yield from self._connection_instance.get_connection()
		yield from self._connection.lpush(queue_name,payload)
		return payload
	@asyncio.coroutine
	def dequeue(self,queue_name):
		if not self._connection:
			self._connection=yield from self._connection_instance.get_connection()
		payload=yield from self._connection.rpop(queue_name)
		if payload and isinstance(payload,bytes):
			payload=payload.encode("utf-8")
		elif not payload:
			payload=[]
		return payload
	@asyncio.coroutine
	def close_queue(self):
		if self._connection_instance:
			yield from self._connection_instance.close()
class AsyncMysqlQueue(AsyncQueue):
	_queue_list=tuple()
	def __init__(self,config,loop,connection=AsyncMysqlConnection):
		assert isinstance(config,dict)
		super(AsyncMysqlQueue,self).__init__(config)
		self._loop=loop
		self._queue_conn=None
		self._connection_instance=connection(self._host,self._port,self._user,self._password,self._db)
	def _check_queue(self,queue_name):
		if queue_name in self._queue_list:
			return True
		return False
	@asyncio.coroutine
	def _get_queue_list(self):
		cursor=yield from self._queue_conn.cursor()
		yield from cursor.execute('show tables')
		tables=yield from cursor.fetchall()
		queue_list=[]
		for table in tables:
			queue_list.append(table[0])
		self._queue_list=tuple(queue_list)
		return self._queue_list
	@asyncio.coroutine
	def _create_queue(self,queue_name):
		cursor=yield from self._queue_conn.cursor()
		yield from self._queue_conn.begin()
		try:
			yield from cursor.execute('create table `%s`(`id` int unsigned not null auto_increment primary key,`payload` longtext )charset utf8'%(queue_name))
		except Exception:
			yield from self._queue_conn.rollback()
		finally:
			yield from self._queue_conn.commit()
			yield from cursor.close()
	@asyncio.coroutine
	def _check_connection(self):
		if not self._queue_conn:
			self._queue_conn=yield from self._connection_instance.get_connection(self._loop)
			yield from self._queue_conn.select_db(self._db)
			yield from self._get_queue_list()	
		return self._queue_conn
	@asyncio.coroutine
	def enqueue(self,queue_name,payload):
		assert isinstance(queue_name,str)
		yield from self._check_connection()
		if not self._check_queue(queue_name):
			yield from self._create_queue(queue_name)
			yield from self._get_queue_list()
		cursor=yield from self._queue_conn.cursor()
		yield from self._queue_conn.begin()
		try:
			yield from cursor.execute("insert into `%s` (`payload`) values('%s')"%(queue_name,payload))
		except Exception as e:
			yield from self._queue_conn.rollback()
		finally:
			yield from self._queue_conn.commit()
			yield from cursor.close()
		return payload
	@asyncio.coroutine
	def dequeue(self,queue_name):
		assert isinstance(queue_name,str)
		assert isinstance(payload,(str,bytes))
		yield from self._check_connection()
		if not self._check_queue(queue_name):
			yield from self._create_queue(queue_name)
			yield from self._get_queue_list()
		cursor=yield from self._queue_conn.cursor()
		yield from cursor.execute('select `id`,`payload` from `%s` order by `id` asc limit 1'%(queue_name))
		ret=yield from cursor.fetchone()
		if ret and len(ret)>=1:
			try:
				yield from cursor.execute("delete from `%s` where `id`=%s"%(queue_name,ret[0]))
			except Exception:
				yield from self._queue_conn.rollback()
			finally:
				yield from self._queue_conn.commit()
				yield from cursor.close()
			return ret[1]
		return []
	@asyncio.coroutine
	def close_queue(self):
		if self._connection_instance:
			yield from self._connection_instance.close()
class AsyncQueueOperator(object):
	_queue_driver_class={'mysql':AsyncMysqlQueue,'redis':AsyncRedisQueue}
	def __init__(self):
		pass
	def _get_mysql_queue_driver(self,config):
		return self._queue_driver_class.get('mysql')(config,self._loop)
	def _get_redis_queue_driver(self,config):
		return self._queue_driver_class.get("redis")(config,self._loop)
class AsyncQueueReader(AsyncQueueOperator):
	def __init__(self,config,loop,driver_name='mysql'):
		assert isinstance(config,dict)
		assert isinstance(driver_name,str)
		self._loop=loop
		self._reader_instance=getattr(self,"_get_%s_queue_driver"%driver_name)(config)
	@asyncio.coroutine
	def read_from_queue(self,queue_name):
		ret=yield from self._reader_instance.dequeue(queue_name)
		return ret
	@asyncio.coroutine
	def close_reader(self):
		yield from self._reader_instance.close_queue()
class AsyncQueueWriter(AsyncQueueOperator):
	def __init__(self,config,loop,driver_name='mysql'):
		assert isinstance(config,dict)
		assert isinstance(driver_name,str)
		self._loop=loop
		self._writer_instance=getattr(self,"_get_%s_queue_driver"%driver_name)(config)
	@asyncio.coroutine
	def write_to_queue(self,queue_name,payload):
		yield from self._writer_instance.enqueue(queue_name,payload)
		return payload
	@asyncio.coroutine
	def close_writer(self):
		yield from self._writer_instance.close_queue()

class AsyncTask(object):
	def __init__(self,task_type,tries,content,loop,config=None,driver_name=None,encapsulator=QueuePayloadJsonEncapsulator,writer=AsyncQueueWriter):
		assert isinstance(content,(str,dict))
		assert isinstance(task_type,str)
		assert isinstance(tries,int)
		self._content=content
		self._task_type=task_type
		self._tries=tries
		self._encapsulator=encapsulator(self._task_type,self._tries,self._content)
		self._writer=AsyncQueueWriter(config or Config.queue.all,loop,driver_name or Config.queue.driver_name)
	@asyncio.coroutine
	def start(self,queue_name=None):
		if not queue_name:
			queue_name=self._task_type
		data=yield from self._writer.write_to_queue(queue_name,self._encapsulator.encapsulate())
		yield from self._writer.close_writer()
	def refresh_task(self,task_type,tries,content):
		assert isinstance(task_type,str)
		assert isinstance(tries,int)
		assert isinstance(content,(str,dict))
		self._tries=tries
		self._task_type=task_type
		self._content=content
	
if __name__=='__main__':
	r'''
	@asyncio.coroutine
	def go(loop,config=None):
		#asyncqueue=AsyncMysqlQueue(loop,config)
		#data=yield from asyncqueue.enqueue("msg",'shabi')
		#print(data)
		#asyncqueuewriter=AsyncQueueWriter(loop,config)
		#data=yield from asyncqueuewriter.write_to_queue('mail','send mail to you')
		#asyncreader=AsyncQueueReader(loop,config)
		#data=yield from asyncreader.read_from_queue("msg")
		#print(data)
		asynctask=AsyncTask('mail',3,'send mail to 18281573692@163.com',loop,config,'mysql')
		yield from asynctask.start()

	loop=asyncio.get_event_loop()
	config={
		'host':'127.0.0.1',
		'port':3306,
		'user':'root',
		'password':'526114',
		'db':'queue'
	}
	loop.run_until_complete(go(loop,config))
	loop.close()
	'''
