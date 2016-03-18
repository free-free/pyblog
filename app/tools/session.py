#-*- coding:utf-8 -*-

import uuid
import time
import os
import json
import logging

logging.basicConfig(level=logging.ERROR)

try:
	import redis
except ImportError:
	logging.error("Can't import 'redis' module")
try:
	import pymongo
except ImportError:
	logging.error("Can't import 'pymongo' module")
from pymongo import MongoClient
class Session(object):
	def __init__(self,session_id=None):
		if session_id==None:
			self._session_id=self._generate_session_id()
		else:
			self._session_id=session_id
		super(Session,self).__init__()
	def _generate_session_id(self):
		return str(uuid.uuid1().hex)	
	def __getattr__(self,k):
		pass
	def __setattr__(self,k,v):
		pass
	@property
	def session_id(self):
		return self._session_id
	def set(self,sname,svalue):
		pass
	def get(self,sname):
		pass
	def save(self,expire=None):
		pass
	def renew(self,session_id):
		pass
	def __getitem__(self,key):
		pass
	def __setitem__(self,key,value):
		pass
class FileSession(Session):
	r'''	
		session store in file
		file session driver

		session expire file is place  to store session expire time,the file's content  is actually
		a json array,array's formation is following:
			[{'session_info':['7437843aefb48938943394',12232831]},{'session_info':['4387812787abcdf43e32d',12323233232]}]
		first item is session id and second  is expire timestamp in each  dict
	'''
	_session_dir='/tmp/session'
	_session_expire_file='/tmp/session/session_expire'
	_data={}
	#_session_expire_key='session_expire'
	def __init__(self,session_id=None,config=None):
		if not os.path.exists(self._session_dir):
			os.mkdir(self._session_dir)
		if session_id==None:
			self._session_id=self._generate_session_id()
		else:
			self._session_id=session_id
		
		#if os.path.exists(self._session_expire_file):
		#	with open(self._session_expire_file,'r',errors='ignore',encoding='utf-8') as f:
		#		self[self._session_expire_key]=json.load(f)
		#	expire_session=self[self._session_expire_key]
		#	for expire_item in expire_session:
		#		if int(expire_item['session_info'][1])<int(time.time()):
		#			os.remove(os.path.join(self._session_dir,expire_item['session_info'][0]))
		#			self[self._session_expire_key].remove(expire_item)
		#else:
		#	self[self._session_expire_key]=[]
		
		self._session_file=os.path.join(self._session_dir,self._session_id)
		if os.path.exists(self._session_file):	
			with open(self._session_file,'r',errors='ignore',encoding='utf-8') as f:
				self._data[self._session_id]=json.load(f)
			expire=self._data[self._session_id].get('expire',None)
			if expire:
				if int(expire)<int(time.time()):
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
		if expire:
			self.data[self._session_id]['expire']=int(time.time())+int(expire)
			with open(self._session_expire_file,'a+',errors='ignore',encoding='utf-8') as f:
				f.write("%s:%s\r\n"%(self._session_id,int(time.time())+int(expire)))
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
			expire=self._data[self._session_id].get('expire',None)
			if expire:
				if int(expire)<int(time.time()):
					os.remove(self._session_file)
					self._data[self._session_id]={}
		else:
			self._data[self._session_id]={}
		return self
	def __getitem__(self,key):
		return self.data[self._session_id].get(key)
	def __setitem__(self,key,value):
		self._data[self._session_id][key]=value
class MongoSession(Session):
	r'''
		mongodb driver for session
	'''
	_data={}
	def __init__(self,session_id=None,config=None):
		if not config:
			client=MongoClient('localhost',27017)
			self._mongo=client['session_database']['session']
		else:
			if not isinstance(config,dict):
				raise TypeError("mongo session config must be dict type")
			client=MongoClient(config['host'],config['port'])
			self._mongo=client[config['db']][config['collection']]
		if session_id==None:
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
		super(MongoSession,self).__init__(session_id)
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
		self._mongo.update_one({'session_id':self._session_id},{"$set":self._data[self._session_id]},upsert=True)

	def __getitem__(self,key):
		return self._data[self._session_id].get(key)
	def __setitem__(self,key,value):
		self._data[self._session_id][key]=value
class RedisSession(Session):
	r'''
		redis driver for session
	'''
	_pool=None
	_data={}
	def __init__(self,session_id=None,config=None):
		if config==None:
			if not type(self)._pool:
				type(self)._pool=redis.ConnectionPool(host='localhost',port=6379,db=0)
		else:
			if not isinstance(config,dict):
				raise TypeError("redis config must be a dict type")
			if not type(self)._pool:
				type(self)._pool=redis.ConnectionPool(host=config['host'],port=config['port'],db=config['db'])
		if session_id==None:
			self._session_id=self._generate_session_id()
		else:
			self._session_id=session_id
		self._redis=redis.Redis(connection_pool=type(self)._pool)
		self._data[self._session_id]=self._redis.hgetall(self._session_id)
		if not self._data.get(self._session_id):
			self._data[self._session_id]={}
		super(RedisSession,self).__init__(self._session_id)
	def get(self,sname):
		return self._data[self._session_id].get(sname.encode('utf-8'))
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
		return self
	def  save(self,expire=None):
		if expire==None:
			self._redis.hmset(self._session_id,self._data[self._session_id])
		else:
			self._redis.hmset(self._session_id,self._data[self._session_id])
			self._redis.expire(self._session_id,expire)

	def __getitem__(self,key):
		return self._data[self._session_id].get(key)
	def __setitem__(self,key,value):
		self._data[self._session_id][key]=value
class SessionManager(object):
	_drivers={}
	_default_driver=None
	_specific_driver=None
	def __init__(self,session_id=None,config=None,driver=None):
		self._session_id=session_id
		if not driver:
			self._default_driver=self.get_filesession_driver(config)
		else:
			self._default_driver=eval('self.get_%ssession_driver(%s)'%(driver,config))
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
			self._drivers[driver_name]= eval('self.get_%ssession_driver(%s)'%(driver_name,config))
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
			self._specific_driver=None
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
if __name__=='__main__':
	r'''
	filesession=SessionManager()
	filesession.set('name','huangbiao')
	filesession.set('email','19941222hb@gmail.com')
	filesession.save()
	redissession=filesession.driver('redis')
	redissession.set('name','huangbiao')
	redissession.set('email','18281573692@163.com')
	print(redissession.session_id)
	redissession.save()
	'''
	r'''
	redis=SessionManager(driver='redis')
	redis.set('name','jell')
	redis.set('email','1462086237@qq.com')
	redis.save(30)
	'''
	'''
	redis=SessionManager('55e5bf8ce9fc11e5b902080027116c59',driver='redis')
	print(redis.get('name'))
	print(redis.get('email'))
	'''
	redis=SessionManager(driver='redis')
	#file.set('name','dede')
	#file.set('age',32)
	redis['name']='jell'
	redis['age']=21
	redis.save()
	#file.renew().set('name','xiaoming').set('age',48).save()
