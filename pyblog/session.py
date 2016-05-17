#-*- coding:utf-8 -*-

import uuid
import time
import os
import json
import logging
import asyncio
logging.basicConfig(level=logging.ERROR)
import redis
import pymongo
import aioredis
from pymongo import MongoClient

class AbstractSession(object):
	def __init__(self,session_id,*args,**kw):
		self._session_id=session_id
		super(AbstractSession,self).__init__(*args,**kw)
	def _generate_session_id(self,generate_session_id_func=None,*args):
		r''' generate session id'''
		if not generate_session_id_func:
			return str(uuid.uuid1().hex)
		else:
			return str(generate_session_id_func(*args))
	@property
	def session_id(self):
		r''' return session id'''
		return self._session_id
	def set(self,sname,svalue):
		r''' set session item'''
		raise NotImplementedError
	def get(self,sname):
		r''' get session item'''
		raise NotImplementedError
	def save(self,expire=None):
		r''' save all session items to database or file'''
		raise NotImplementedError
	def renew(self,session_id):
		r''' refresh session id and reread session from database'''
		raise NotImplementedError
	def all(self):
		r''' get all session '''
		return self._data[self._session_id]
	def __getitem__(self,key):
		r''' get session item by name'''
		pass
	def __setitem__(self,key,value):
		r''' set session item by name'''
		pass
	def __delitem__(self,key):
		r''' delete session item by name'''
		pass
class AsyncAbstractSession(dict):
	def __init__(self,session_id,*args,**kw):
		if not session_id:
			session_id=self._generate_session_id()
		self._session_id=session_id
		super(AsyncAbstractSession,self).__init__(*args,**kw)
	def _generate_session_id(self,generate_session_id_func=None,*args):
		if not generate_session_id_func:
			return str(uuid.uuid1().hex)
		else:
			return str(generate_session_id_func(*args))
	@asyncio.coroutine
	def save(self,expire=None):
		r''' save session to database'''
		raise NotImplementedError
	@asyncio.coroutine
	def session(self):
		r''' get database connection and read session from database'''
		raise NotImplementedError
	def get(self,sname):
		raise NotImplementedError
	def set(self,sname,value):
		raise NotImplementedError
	def all(self):
		raise NotImplementedError
	@property
	def session_id(self):
		return self._session_id

class AsyncRedisSession(AsyncAbstractSession):
	def __init__(self,session_id=None,config=None,loop=None):
		super(AsyncRedisSession,self).__init__(session_id)
		if not config:
			self._host='localhost'
			self._port=6379
			self._db=0
			self._expire=0
		else:
			assert isinstance(config,dict),"redis connection config must dict type"
			self._host=config.get("host")
			self._port=config.get("port")
			self._db=config.get("db",0)
			self._expire=config.get('expire',0)
		self._connection=None
		self._active=False
		self._loop=loop
	@asyncio.coroutine
	def session(self,loop=None):
		if loop:
			self._loop=loop
		if not self._connection:
			self._connection=yield from aioredis.create_redis((self._host,self._port),loop=self._loop)
			self._active=True
		self[self._session_id]=yield from self._connection.hgetall(self._session_id)
		if not self[self._session_id]:
			self[self._session_id]={}
		else:
			expire_delta_time=self[self._session_id].get(b"__expire_delta_time",b'').decode("utf-8")
			if expire_delta_time:
				yield from self._connection.expire(self._session_id,int(expire_delta_time))
		return self
	def set(self,sname,svalue):
		self[self._session_id][sname]=svalue
		return self
	def get(self,sname):
		return self[self._session_id].get(sname.encode("utf-8"),b'').decode("utf-8")
	@asyncio.coroutine
	def save(self,expire=None):	
		if expire:
			self[self._session_id]['__expire_delta_time']=int(expire)
			pipe=self._connection.pipeline()	
			for key,value in self[self._session_id].items():
				pipe.hset(self._session_id,key,value)
			yield from pipe.execute()
			yield from self._connection.expire(self._session_id,int(expire))
		else:	
			if int(self._expire)!=0:
				self[self._session_id]['__expire_delta_time']=self._expire	
				pipe=self._connection.pipeline()
				for key,value in self[self._session_id].items():
					pipe.hset(self._session_id,key,value)
				yield from pipe.execute()
				yield from self._connection.expire(self._session_id,self._expire)
			else:
				pipe=self._connection.pipeline()
				for key,value in self[self._session_id].items():
					pipe.hset(self._session_id,key,value)
				yield from pipe.execute()	
	@asyncio.coroutine
	def end(self):
		if self._connection:
			self._connection.close()
			yield from self._connection.wait_closed()
	def all(self):
		return self[self._session_id]
class FileSession(AbstractSession):
	r'''	
		session store in file
		file session driver

		session expire file is place  to store session expire time,the file's content  is actually
		a json array,array's formation is following:
			[{'session_info':['7437843aefb48938943394',12232831]},{'session_info':['4387812787abcdf43e32d',12323233232]}]
		first item is session id and second  is expire timestamp in each  dict
	'''
	_data={}
	def __new__(cls,*args,**kw):
		if not hasattr(cls,'_instance'):
			cls._instance=super(AbstractSession,cls).__new__(cls)
		return cls._instance
	def __init__(self,session_id=None,config=None):
		if not config:
			self._session_dir='/tmp/session'
			self._session_expire=0
		else:
			if not isinstance(config,dict):
				raise TypeError("FileSession config must be dict type")
			self._session_dir=config.get('session_dir','/tmp/session')
			self._session_expire=int(config.get('expire',0))

		if not os.path.exists(self._session_dir):
			os.mkdir(self._session_dir)
		if session_id==None:
			self._session_id=self._generate_session_id()
		else:
			self._session_id=session_id
		self._session_file=os.path.join(self._session_dir,self._session_id)
		if os.path.exists(self._session_file):	
			with open(self._session_file,'r',errors='ignore',encoding='utf-8') as f:
				self._data[self._session_id]=json.load(f)
			expire_time=self._data[self._session_id].get('__expire_delta_time',None)
			last_active_time=self._data[self._session_id].get('__last_active_time')
			if expire_time:
				if (int(time.time())-(last_active_time))>expire_time:
					os.remove(self._session_file)
					self._data[self._session_id]={}
		else:
			self._data[self._session_id]={}
		super(FileSession,self).__init__(self._session_id)
	def set(self,sname,svalue):
		self._data[self._session_id][sname]=svalue
		return self
	def get(self,sname):
		return self._data[self._session_id].get(sname,None)
	def save(self,expire=None):
		current_time=int(time.time())
		self._data[self._session_id]['__last_active_time']=current_time
		if expire:
			self._data[self._session_id]['__expire_delta_time']=int(expire)
		else:
			if int(self._session_expire)!=0:
				self._data[self._session_id]['__expire_delta_time']=self._session_expire
		with open(self._session_file,'w',errors='ignore',encoding='utf-8') as f:
			json.dump(self._data[self._session_id],f)
		
	def renew(self,session_id=None):
		if session_id==None:
			self._session_id=self._generate_session_id()
		else:	
			self._session_id=session_id
		self._session_file=os.path.join(self._session_dir,self._session_id)
		if os.path.exists(self._session_file):
			with open(self._session_file,'r',errors='ignore',encoding='utf-8') as f:
				self._data[self._session_id]=json.load(f)
			expire_time=self._data[self._session_id].get('__expire_delta_time',None)
			last_active_time=self._data[self._session_id].get('__last_expire_time')
			if expire_time:
				if (int(time.time)-last_active_time)>expire_time:
					os.remove(self._session_file)
					self._data[self._session_id]={}
		else:
			self._data[self._session_id]={}
		return self
	def delete(self,session_id=None):
		if session_id:
			if session_id in self._data:
				del self._data[session_id]
			if session_id in os.listdir(self._session_dir):
				os.remove(os.path.join(self._session_dir,session_id))	
			return session_id
		else:
			ssid=self._session_id
			del self._data[self._session_id]
			if self._session_id in os.listdir(self._session_dir):
				os.remove(os.path.join(self._session_dir,self._session_id))
			self._session_id=self._generate_session_id()
			self._data[self._session_id]={}
			return ssid
	def __getitem__(self,key):
		return self._data[self._session_id].get(key)
	def __setitem__(self,key,value):
		self._data[self._session_id][key]=value
class MongoSession(AbstractSession):
	r'''
		mongodb driver for session
	'''
	_data={}
	def __init__(self,session_id=None,config=None):
		if not config:
			self._host='localhost'
			self._port=27017
			self._db='session_database'
			self._collection='session'
			self._expire=0
		else:
			if not isinstance(config,dict):
				raise TypeError("mongo session config must be dict type")
			self._host=config.get('host','localhost')
			self._port=config.get('port',27017)
			self._db=config.get('db','session_database')
			self._collection=config.get('collection','session')
			self._expire=config.get('expire',0)
		client=MongoClient(self._host,self._port)
		self._mongo=client[self._db][self._collection]
		if session_id==None:
			self._session_id=self._generate_session_id()
		else:
			self._session_id=session_id
		self._data[self._session_id]=dict(self._mongo.find_one({'session_id':self._session_id}))
		expire=self._data[self._session_id].get('expire',None)
		if not self._data.get(self._session_id):
			self._data[self._session_id]={}
		else:
			if expire:
				if int(expire)<int(time.time()):
					self._data[self._session_id]={}
		super(MongoSession,self).__init__(self._session_id)
	def get(self,sname):
		return self._data[self._session_id].get(sname)
	def set(self,sname,svalue):
		self._data[self._session_id][sname]=svalue
		return self
	def renew(self,session_id):
		if not session_id:
			self._session_id=self._generate_session_id()
		else:
			self._session_id=session_id
		self._data[self._session_id]=self._mongo.find_one({'session_id':self._session_id})
		expire=self._data[self._session_id].get('expire',None)
		if not self._data.get(self._session_id):
			self._data[self._session_id]={}
		else:
			if expire:
				if int(expire)<int(time.time()):
					self._data[self._session_id]={}
		return self
	def save(self,expire=None):
		if  expire:
			self._data[self._session_id]['expire']=int(expire)+int(time.time())
		else:
			if int(self._expire)!=0:
				self._data[self._session_id]['expire']=int(time.time())+int(expire)
		self._mongo.update_one({'session_id':self._session_id},{"$set":self._data[self._session_id]},upsert=True)
	def delete(self,session_id=None):
		if session_id:
			if session_id in self._data:
				del self._data[session_id]
			session=self._mongo.find_one_and_delete({'session_id':session_id},projection={'session_id':True})
			return session.get('session_id')
		else:
			del self._data[self._session_id]
			session=self._mongo.find_one_and_delete({'session_id':self._session_id},projection={'session_id':True})
			self._session_id=self._generate_session_id()
			self._data[self._session_id]={}
			return  session.get('session_id')
	def __getitem__(self,key):
		return self._data[self._session_id].get(key)
	def __setitem__(self,key,value):
		self._data[self._session_id][key]=value
class RedisSession(AbstractSession):
	r'''
		redis driver for session
	'''
	_pool=None
	_data={}
	def __init__(self,session_id=None,config=None):
		if config==None:
			self._host='localhost'
			self._port=6379
			self._db=0
			self._expire=0
		else:
			if not isinstance(config,dict):
				raise TypeError("redis config must be a dict type")
			self._host=config.get('host','localhost')
			self._port=config.get('port',6379)
			self._db=config.get('db',0)
			self._expire=config.get('expire',0)
		if not type(self)._pool:
			type(self)._pool=redis.ConnectionPool(host=self._host,port=self._port,db=self._db)
		if session_id==None:
			self._session_id=self._generate_session_id()
		else:
			self._session_id=session_id
		self._redis=redis.Redis(connection_pool=type(self)._pool)
		self._data[self._session_id]=self._redis.hgetall(self._session_id)
		if not self._data.get(self._session_id):
			self._data[self._session_id]={}
		else:
			expire_delta_time=self._data[self._session_id].get('__expire_delta_time'.encode('utf-8'),b'').decode('utf-8')
			if expire_delta_time:
				self._redis.expire(self._session_id,int(expire_delta_time))
		super(RedisSession,self).__init__(self._session_id)
	def get(self,sname):
		return self._data[self._session_id].get(sname.encode('utf-8'),b'').decode('utf-8')
	def set(self,sname,svalue):
		self._data[self._session_id][sname]=svalue
		return self
	def renew(self,session_id=None):
		if session_id==None:
			self._session_id=self._generate_session_id()
		else:
			self._session_id=session_id
		self._data[self._session_id]=self._redis.hgetall(self._session_id)
		if not self._data.get(self._session_id):
			self._data[self._session_id]={}
		else:	
			expire_delta_time=self._data[self._session_id].get('__expire_delta_time'.encode('utf-8'),b'').decode('utf-8')
			if expire_delta_time:
				self._redis.expire(self._session_id,int(expire_delta_time))
		return self
	def  save(self,expire=None):
		if expire:
			self._data[self._session_id]['__expire_delta_time']=int(expire)
			self._redis.hmset(self._session_id,self._data[self._session_id])
			self._redis.expire(self._session_id,int(expire))
		else:	
			if int(self._expire)!=0:
				self._data[self._session_id]['__expire_delta_time']=self._expire	
				self._redis.hmset(self._session_id,self._data[self._session_id])
				self._redis.expire(self._session_id,self._expire)
			else:
				self._redis.hmset(self._session_id,self._data[self._session_id])
	def delete(self,session_id=None):
		if session_id:
			if session_id in self._data:
				del self._data[session_id]
			keys=self._redis.hkeys(session_id)
			if keys:
				self._redis.hdel(session_id,*keys)
			return session_id
		else:
			ssid=self._session_id
			del self._data[self._session_id]
			keys =self._redis.hkeys(self._session_id)
			if keys:
				self._redis.hdel(self._session_id,*keys)
			self._session_id=self._generate_session_id()
			self._data[self._session_id]={}
			return ssid	
	def __getitem__(self,key):
		return self.get(key)
	def __setitem__(self,key,value):
		self.set(key,value)
class AsyncSessionManager(object):
	def __init__(self,session_id=None,*,config=None,driver=None):
		pass
	def _get_redis_session_driver(self,config=None):
		pass
class SessionManager(object):
	_drivers={}
	_default_driver=None
	_specific_driver=None
	def __init__(self,session_id=None,*,config=None,driver=None):
		self._session_id=session_id
		if not driver:
			self._default_driver=self.get_filesession_driver(config)
		else:
			self._default_driver=getattr(self,'get_%ssession_driver'%driver)(config)
	def get_mongosession_driver(self,config=None):
		type(self)._drivers['mongo']=MongoSession(self._session_id,config)
		return type(self)._drivers['mongo']
	def get_redissession_driver(self,config=None):
		type(self)._drivers['redis']=RedisSession(self._session_id,config)
		return type(self)._drivers['redis']
	def get_filesession_driver(self,config=None):
		type(self)._drivers['file']=FileSession(self._session_id,config)
		return type(self)._drivers['file']
	def driver(self,driver_name,config=None):
		if driver_name in self._drivers:		
			self._specific_driver=self._drivers[driver_name]
		else:
			self._drivers[driver_name]=getattr(self,'get_%ssession_driver'%driver_name)(config)
			self._specific_driver=self._drivers[driver_name]
		return self
	def get(self,sname):
		if not self._specific_driver:
			return self._default_driver.get(sname)
		else:
			return self._specific_driver.get(sname)
	def set(self,sname,value):
		if not self._specific_driver:
			self._default_driver.set(sname,value)
		else:
			self._specific_driver.set(sname,value)
		return self
	def save(self,expire=None):
		if not self._specific_driver:
			self._default_driver.save(expire)
		else:
			self._specific_driver.save(expire)
	def renew(self,session_id=None):
		if not self._specific_driver:
			self._default_driver.renew(session_id)
		else:
			self._specific_driver.renew(session_id)
		return self
	@property
	def session_id(self):
		if not self._specific_driver:
			return self._default_driver.session_id
		else:
			return self._specific_driver.session_id
	def __setitem__(self,key,value):
		if not self._specific_driver:
			self._default_driver[key]=value
		else:
			self._specific_driver[key]=value
	def __getitem__(self,key):
		if not self._specific_driver:
			return self._default_driver[key] 
		else:
			return self._specific_driver[key]
	def delete(self,session_id=None):
		if not self._specific_driver:
			return self._default_driver.delete(session_id)
		else:
			return self._specific_driver.delete(sesion_id)
	def all(self):
		if not self._specific_driver:
			return self._default_driver.all()
		else:
			return self._specfic_driver.all()
if __name__=='__main__':
	pass

	r'''
	@asyncio.coroutine
	def go():
		asyncsession=yield from AsyncRedisSession().session()
		asyncsession.set("name","huangbiao").set("age",22)
		print(asyncsession.get("age"))
		yield from asyncsession.save(40)
		yield from asyncsession.end()
	loop=asyncio.get_event_loop()
	loop.run_until_complete(go())
	loop.close()
	'''
	r'''
	#file=SessionManager()
	#file.set('name','Jell')
	#file.set('email','dejiejfioe@gmail.com')
	#file.save(20)	
	#file=SessionManager("c56fbc34fee411e5afc6080027116c59")
	#print(file['name'])
	#print(file['email'])
	#redis=SessionManager(driver='redis')
	#redis.set('name','huangbiao')
	#redis.set('email','18281573692@163.com')
	#print(redis.session_id)
	#redis.save(60)
	#redis=SessionManager("4f9f0a42fee811e59da2080027116c59",driver='redis')
	#print(redis['email'])
	#print(redis['name'])
	#print(redis.session_id)
	#print(redis.delete())
	#redis=SessionManager(driver='redis')
	#redis['name']='xiaohong'
	#redis['age']=100
	#redis.delete("be3f28feed9711e5a0a5080027116c59")
	#redis.save(10)
	#print(redis.delete())

	#file=SessionManager("a9beba48ed9211e582f4080027116c59")
	#print(file.session_id)
	#file.delete()
	
	#file.renew().set('name','xiaoming').set('age',48).save()
	'''
