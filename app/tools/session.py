#-*- coding:utf-8 -*-

import uuid
import time
import os
import json
class Session(dict):
	def __init__(self,session_id=None,expire=None,*args,**kw):
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
class FileSession(Session):
	_sesion_dir='/tmp/session'
	def __init__(self,session_id=None,expire=None,*args,**kw):
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
				self[self._session_id]=json.load(self._fp)
		else:
			self[self._session_id]={}
		super(FileSession,self).__init__(self._session_id,expire,*args,**kw)
	def set(self,sname,svalue):
		self[self._session_id][sname]=svalue
	def get(self,sname):
		return self[self._session_id].get(sname,None)
	def save(self):
		with open(self._session_file,'w',errors='ignore',encoding='utf-8') as f:
			json.dump(self[self._session_if],f)
	def __getattr__(self,k):
		if k in self[self._session_id]:
			return self[self._session_id].get(k)
		return None
	def __setattr__(self,k,v):
		self[self._session_id][k]=v

class MongoSession(Session):
	def __init__(self,session_id=None,expire=None,*args,**kw):
		super(MongoSession,self).__init__(session_id,expire,*args,**kw)
class RedisSession(Session):
	def __init__(self,session_id=None,expire=None,*args,**kw):
		super(RedisSession,self).__init__(session_id,expire,*args,**kw)

class SessionManager(object):
	def __init__(self,

		
