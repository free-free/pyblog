#-*- coding:utf-8 -*-
import logging
logging.basicConfig(level=logging.ERROR)
import time
import json
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
	_db_check=False
	def __init__(self):
		pass
	def _create_connection(self,host,port,user,password):
		type(self)._connection=MySQLdb.connect(host=host,port=port,user=user,passwd=password)
		return type(self)._connection
	@property
	def _check_connection(self):
		if not type(self)._connection:
			return False
		return True
	def _check_db(self,queue_db):
		if not type(self)._db_check:
			cursor=type(self)._connection.cursor()
			cursor.execute('show databases')
			alldatabases=cursor.fetchall()
			cursor.close()
			for db in alldatabases:
				if queue_db==db[0]:
					type(self)._db_check=True
					break
		return type(self)._db_check
	def _create_db(self,queue_db):
		cursor=type(self)._connection.cursor()
		cursor.execute('create database `%s` character set utf8'%queue_db)
		cursor.close()
		type(self)._connection.commit()
	def __get__(self,obj,ownclass):
		if not self._check_connection:	
			self._create_connection(obj._host,obj._port,obj._user,obj._password)
			if not self._check_db(obj._db):
				self._create_db(obj._db)
			type(self)._connection.select_db(obj._db)
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
			raise AttributeError("%s has no such '%s' attirbute"%(type(self),key))
class RedisQueue(Queue):
	_redis_conn=RedisConnection()
	def __init__(self,config=None):
		if not config:	
			config=dict()
			config['host']='localhost'
			config['port']=6379
			config['db']=0
		super(RedisQueue,self).__init__(config)
	def enqueue(self,queue_name,payload):
		self._redis_conn.lpush(queue_name,payload)
		return payload
	def dequeue(self,queue_name):
		payload=self._redis_conn.rpop(queue_name)
		if isinstance(payload,bytes):
			payload=payload.decode('utf-8')
		return payload
class MongoQueue(Queue):
	_mongo_conn=MongoConnection()
	def __init__(self,config=None):
		if not config:
			config=dict()
			config['host']='localhost'
			config['port']=27017
			config['db']='queue'
		super(MongoQueue,self).__init__(config)
	def enqueue(self,queue_name,payload):
		self._mongo_conn[queue_name].insert_one({'id':time.time(),'payload':payload})
		return content
	def dequeue(self,queue_name):
		data=self._mongo_conn[queue_name].find().sort('id',1).limit(1)
		ret=[]
		for item in data:
			ret.append(item)
		if ret and len(ret)>=1:
			self._mongo_conn[queue_name].remove({"id":ret[0]['id']})
			return ret[0]['payload']
		return ''
class MysqlQueue(Queue):
	_mysql_conn=MysqlConnection()
	_queue_check=False
	_all_queues=tuple()
	def __init__(self,config=None):
		if not config:
			config=dict()
			config['port']=3306
			config['host']='localhost'
			config['db']='queue'
			config['user']='root'
			config['password']='526114'
		super(MysqlQueue,self).__init__(config)
	def _get_all_queues(self):
		cursor=self._mysql_conn.cursor()
		cursor.execute('show tables')
		alltables=cursor.fetchall()
		allqueues=list()
		for table in alltables:
			allqueues.append(table[0])
		type(self)._all_queues=tuple(allqueues)
		return type(self)._all_queues
	def _check_queue(self,queue_name):
		if not type(self)._queue_check:
			self._get_all_queues()
			type(self)._queue_check=True
		if queue_name not in type(self)._all_queues:
			self._create_queue(queue_name)
			self._get_all_queues()
			print(type(self)._all_queues)
		return True
	def _create_queue(self,queue_name):
		cursor=self._mysql_conn.cursor()
		cursor.execute('create table `%s`( `id` int unsigned not null auto_increment primary key,`payload` longtext)charset utf8'%(queue_name))
		cursor.close()
	def enqueue(self,queue_name,payload):
		self._check_queue(queue_name)
		cursor=self._mysql_conn.cursor()
		cursor.execute("insert into `%s`(`payload`) values('%s')"%(queue_name,payload))
		cursor.close()
		self._mysql_conn.commit()
		return content
	def dequeue(self,queue_name):
		self._check_queue(queue_name)
		cursor=self._mysql_conn.cursor()
		cursor.execute('select * from `%s` order by `id` asc limit 1'%queue_name)
		ret=cursor.fetchone()
		if ret and len(ret)>=1:
			cursor.execute('delete from `%s` where `id`=%s'%(queue_name,ret[0]))
			self._mysql_conn.commit()
			cursor.close()
			return ret[1]
		else:
			cursor.close()
			return ''
class QueueOperator(object):
	_queue_driver_class={'redis':RedisQueue,'mongo':MongoQueue,'mysql':MysqlQueue}
	def __init__(self):
		pass
	def _get_redis_queue_driver(self,config=None):
		return self._queue_driver_class.get('redis')(config)
	def _get_mongo_queue_driver(self,config=None):
		return self._queue_driver_class.get('mongo')(config)
	def _get_mysql_queue_driver(self,config=None):
		return self._queue_driver_class.get('mysql')(config)
		
class QueueReader(QueueOperator):
	_queue_read_driver_instance={}
	def __init__(self,driver_name='redis',config=None):
		if config:
			type(self)._queue_read_driver_instance[driver_name.lower()]=eval('self._get_%s_queue_driver(%s)'%(driver_name.lower(),config))
		else:
			if driver_name.lower() not in type(self)._queue_read_driver_instance:
				type(self)._queue_read_driver_instance[driver_name.lower()]=eval('self._get_%s_queue_driver(%s)'%(driver_name.lower(),None))
		self._queue_reader=type(self)._queue_read_driver_instance[driver_name.lower()]
	def read_from_queue(self,queue_name):
		return self._queue_reader.dequeue(queue_name)

class QueueWriter(QueueOperator):
	_queue_write_driver_instance={}
	def __init__(self,driver_name='redis',config=None):
		if config:
			type(self)._queue_write_driver_instance[driver_name.lower()]=eval('self._get_%s_queue_driver(%s)'%(driver_name.lower(),config))
		else:
			if driver_name.lower() not in type(self)._queue_write_driver_instance:
				type(self)._queue_write_driver_instance[driver_name.lower()]=eval('self._get_%s_queue_driver(%s)'%(driver_name.lower(),config))
		self._queue_writer=type(self)._queue_write_driver_instance[driver_name.lower()]
	def write_to_queue(self,queue_name,payload):
		self._queue_writer.enqueue(queue_name,payload)
		return payload

class Executor(object):
	def __init__(self,content,tries):
		self._content=content
		self._tries=tries
	def execute(self):
		pass
	def set_execution_content(self,content,tries):
		self._content=content
		self._tries=tries

class MailExecutor(Executor):
	r'''
		MailExecutor is responsible for to send mail
	'''
	def _get_mail_sender(self):
		pass
	def _get_mail_receiver(self):
		pass
	def _get_mail_title(self):
		pass
	def _get_mail_main(self):
		pass
	def execute(self):
		print(self._content)
		print(self._tries)	

class QueuePayloadParser(object):
	def __init__(self,payload):
		pass
	def get_payload_type(self):
		pass
	def get_payload_createtime(self):
		pass
	def get_payload_tries(self):
		pass
	def get_payload_content(self):
		pass
	def set_payload(self):
		pass

class QueuePayloadJsonParser(QueuePayloadParser):
	r'''
		QueuePayloadParser is class that responsible for parsing the payload reading from queue,
	'''
	def __init__(self,payload):
		if isinstance(payload,str):
			self._payload=json.loads(payload)
		else:
			self._payload={}
		super(type(self),self).__init__(self._payload)
	def get_payload_type(self):
		return self._payload.get('type')
	def get_payload_createtime(self):
		return self._payload.get('create_time')
	def get_payload_tries(self):
		return self._payload.get('tries')
	def get_payload_content(self):
		return self._payload.get('content')
	def set_payload(self,payload):
		self._payload=json.loads(payload)

class QueuePayloadRouter(object):
	r'''
		QueuePayloadRouter is a place where queue payload parser parses the payload ,
		then routes the payload to the related executor.before using QueuePayloadRouter,
		you need to call it's classmethod register_executor() to register your executor
		your  executor must be subclass of Executor abstract class. you also can call class 
		method unregister_executor() to unregister your executor
	'''
	_executor={}
	_executor_instance={}
	_parser_instance=None
	def __init__(self,payload,*,parser=QueuePayloadJsonParser):
		self._payload=payload
		self._parser_class=parser
	def route_to_executor(self):
		#check the parser instance existense
		if not type(self)._parser_instance:
			type(self)._parser_instance=self._parser_class(self._payload)
		else:
			type(self)._parser_instance.set_payload(self._payload)
		payload_type=type(self)._parser_instance.get_payload_type()
		#check payload related executor instance existense
		if payload_type in type(self)._executor_instance:
			self._excutor_instance[payload_type].set_execution_content(self._parser_instance.get_payload_content(),self._parser_instance.get_payload_tries())
		else:
			if payload_type in type(self)._executor:
				type(self)._executor_instance[payload_type]=type(self)._executor[payload_type](self._parser_instance.get_payload_content(),self._parser_instance.get_payload_tries())
			else:
				return False
		#call executor to process payload
		self._executor_instance[payload_type].execute()
		return True
	@classmethod
	def register_executor(cls,**executor):
		for executor_name,executor_class in executor.items():
			cls._executor[executor_name]=executor_class
	@classmethod
	def unregister_executor(cls,executor_name):
		if executor_name in cls._executor:
			del cls._executor[executor_name]
		if executor_name in cls._executor_instance:
			del cls._executor_instance[executor_name]
class QueuePayloadEncapsulator(object):
	def __init__(self,type_name,tries,content):
		self._type=type_name
		self._tries=tries
		self._content=content
		self._payload={}
		self._create_time=time.time()
	def encapsulate(self):
		pass
	def _add_create_time(self,create_time):
		self._payload['create_time']=create_time
	def _add_tries(self,tries):
		self._payload['tries']=tries
	def _add_type(self,type_name):
		self._payload['type']=type_name
	def _add_content(self,content):
		self._payload['content']=content
class QueuePayloadJsonEncapsulator(QueuePayloadEncapsulator):
	r'''
		before sending something to queue,QueuePayloadEncapsulator must be called to encasulate payload
	'''
	def encapsulate(self):
		self._add_create_time(self._create_time)
		self._add_tries(self._tries)
		self._add_type(self._type)
		self._add_content(self._content)
		return self._json_encode(self._payload)
	def _json_encode(self,payload):
		return json.dumps(payload)

class Task(object):
	def __init__(self,task_type,tries,content,*,encapsulator=QueuePayloadJsonEncapsulator,queue_writer=QueueWriter):
		self._task_type=task_type
		self._tries=tries
		self._content=content
		self._encapsulator=encapsulator
		self._writer=queue_writer
	def start(self,queue_name=None):
		if queue_name:
			self._writer().write_to_queue(queue_name,(self._encapsulator(self._task_type,self._tries,self._content).encapsulate()))
		else:
			self._writer().write_to_queue(self._task_type,(self._encapsulator(self._task_type,self._tries,self._content).encapsulate()))

class TaskProcessor(object):				
	def __init__(self,payload_router=QueuePayloadRouter,queue_reader=QueueReader):
		self._router=payload_router
		self._reader=queue_reader
	def process(self,queue_name):
		payload=self._reader().read_from_queue(queue_name)
		self._router(payload).route_to_executor()
	
if __name__=='__main__':
	#QueuePayloadRouter.register_executor(mail=MailExecutor)
	#tsk1=Task('mail',3,'send to mail to 19941222hb@gmail.com')
	#tsk1.start()
	#tsk2=Task('mail',3,'senf to mail to 18281573692@163.com')
	#tsk2.start()
	#tskprcss=TaskProcessor()
	#tskprcss.process('mail')
