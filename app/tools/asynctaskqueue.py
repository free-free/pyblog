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
								loop=loop)
			return self._conn[self._db]
		else:
			if db not in self._conn:
				self._conn[self._db]=yield from aiomysql.connect(host=self._host,
									port=self._port,
									user=self._user,
									password=self._password,
									loop=loop)
			return self._conn[db]
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
	
class AsyncMysqlQueue(AsyncQueue):
	_queue_conn=None
	_db_list=tuple()
	_queue_list=tuple()
	def __init__(self,loop,config,connection=AsyncMysqlConnection):
		assert isinstance(config,dict)
		self._connection_class=connection
		self._loop=loop
		super(MysqlAsyncQueue,self).__init__(config)
	@property
	def _check_queue_db(self,db_name):
		if db_name in self._db_list:
			return True
		return False
	@property
	def _check_queue(self,queue_name):
		if queue_name in self._queue_list:
			return True
		return False
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
	def _create_queue_db(self,db_name):
		cursor=yield from self._queue_conn.cursor()
		yield from self._queue_conn.begin()
		try:
			yield from cursor.execute('create database %s character set utf8'%db_name)
		except Exception:
			yield from self._queue_conn.rollback()
		finally:
			yield from self._queue_conn.commit()
			yield from cursor.close()
			yield from self._queue_conn.select_db(db_name)
	
	@asyncio.coroutine
	def _check_connection(self):
		if not self._queue_conn:
			self._queue_conn=yield from self._connection_class(self._host,self._port,self._user,self._password,self._db).get_connection(self._loop)
			cursor=yield from self._queue_conn.cursor()
			db_list=[]
			yield from cursor.execute("show databases")
			dbs=yield from cursor.fetchall()
			for db in dbs:
				db_list.append(db)
			yield from self._queue_conn.select_db(self._db)
			self._db_list=tuple(db_list)
			yield from cursor.execute("show tables")
			tables=yield from cursor.fetchall()
			queue_list=[]
			for table in tables:
				queue_list.append(table)
			self._queue_list=tuple(queue_list)
			yield from cursor.close()
		return self._queue_conn
	@asyncio.coroutine
	def enqueue(self,queue_name,payload):
		yield from self._check_connection()
		if not self._check_queue_db:
			yield from self._create_queue_db(self._db)
		if not self._check_queue:
			yield from self._create_queue(queue_name)	
		cursor=yield from self._queue_conn.cursor()
		yield from self._queue_conn.begin()
		try:
			yield from cursor.execute('insert into `%s`(`payload`) values(%s)'%(queue_name,payload))
		except Exception:
			yield from self._queue_conn.rollback()
		finally:
			yield from self._queue_conn.commit()
			yield from cursor.close()
		return payload
	@asyncio.coroutine
	def dequeue(self,queue_name):
		yield from self._check_connection()
		cursor=yield from self._queue_conn.cursor()
		yield from self._queue_conn.begin()
		try:
			yield from cursor.execute('select `id`,`payload` from `%s` order by `id` asc limit 1'%(queue_name))
		except Exception:
			yield from self._queue_conn.rollback()
		finally:
			yield from self._queue_conn.commit()
			ret=yield from cursor.fetchone()
			yield from cursor.close()
			if ret and len(ret)>=1:
				return ret[1]
			return []
if __name__=='__main__':
	pass
