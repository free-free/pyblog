#-*- coding:utf-8 -*-

import uuid
import time
import os
import json
class Session(dict):
	def __init__(self,session_id=None,expire=None):
		if session_id==None:
			self._session_id=self._generate_session_id()
		else:
			self._session_id=session_id
		self._expire=expire
		super(Session,self).__init__(*args,**kw)
	def _generate_session_id(self):
		return str(uuid.uuid1().hex)	
	def set(self,sname,svalue):
		pass
	def get(self,sname):
		pass
	def __getattr__(self,k):
		pass
	def __setattr__(self,k,v):
		pass
	def save(self):
		pass
	def renew(self,session_id):
		pass
	def set_expire(self,expire):
		pass
class FileSession(Session):
	r'''	
		session store in file
		file session driver
	'''
	_session_dir='/tmp/session'
	def __init__(self,session_id=None,expire=None,config=None):
		if not os.path.exists(self._session_dir):
			os.mkdir(self._session_dir)
		if session_id==None:
			self._session_id=str(uuid.uuid1().hex)
			self._session_file=os.path.join(self._session_dir,self._session_id)
		else:
			self._session_id=session_id
			self._session_file=os.path.join(self._session_dir,session_id)
		if os.path.exists(self._session_file):	
			with open(self._session_file,'r',errors='ignore',encoding='utf-8') as f:
				self[self._session_id]=json.load(f)
		else:
			self[self._session_id]={}
		super(FileSession,self).__init__(self._session_id,expire)
	def set(self,sname,svalue):
		self[self._session_id][sname]=svalue
	def get(self,sname):
		return self[self._session_id].get(sname,None)
	def save(self):
		with open(self._session_file,'w',errors='ignore',encoding='utf-8') as f:
			json.dump(self[self._session_if],f)
	def renew(self,session_id=None):
		if session_id==None:
			self._session_id=self._generate_session_id()
		else:	
			self._session_id=session_id
		self._session_file=os.path.join(self._session_dir,self._session_id)
		if os.path.exists(self._session_file):
			with open(self._session_file,'r',errors='ignore',encoding='utf-8') as f:
				self[self._session_id]=json.load(f)
		else:
			self[self._session_id]={}
		return self
	def set_expire(self,timeout):
		self._expire=timeout
	def __getattr__(self,k):
		if k in self[self._session_id]:
			return self[self._session_id].get(k)
		return None
	def __setattr__(self,k,v):
		self[self._session_id][k]=v

class MongoSession(Session):
	def __init__(self,session_id=None,expire=None,config=None):
		super(MongoSession,self).__init__(session_id,expire)
class RedisSession(Session):
	def __init__(self,session_id=None,expire=None,config=None):
		super(RedisSession,self).__init__(session_id,expire)

class SessionManager(object):
	_drivers={}
	_default_driver=None
	_specific_driver=None
	def __init__(self,session_id=None,config=None):
		self._session_id=session_id
	def get_mongosession_driver(self,config):
		type(self)._drivers['mongo']=MongoSession(self._session_id,expire,config)
		return type(self)._drivers['mongo']
	def get_redissesssoin_driver(self,config):
		type(self)._drivers['redis']=RedisSession(self._session_id,expire,config)
		return type(self)._drivers['redis']
	def get_filesession_driver(self,config):
		type(self)._drivers['file']=FileSession(self._session_id,expire,config)
		return type(self)._drivers['file']
	def driver(self,driver_name,config):
		if driver_name in self._drivers:		
			self._specific_driver=self._drivers[driver_name]
		else:
			self._specific_driver= eval('self.get_%ssession_driver(%s'%(driver_name,config))
		return self
	
