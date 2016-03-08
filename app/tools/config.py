# -*- coding:utf-8 -*-


class DBConfigLoader(object):
	_config_instance=None
	
	def __new__(cls,*args,**kw):
		if cls._config_instance==None:
			cls._config_instance=object.__new__(cls,*args,**kw)
		return cls._config_instance
	def __init__(self):
		self._config=__import__('conf','app.conf').database
		self._default=self._config['default']
		self._specific=None
	def _get_specific_config_item(self,item_name,connection):
		if item_name in self._config['connections'][connection]:
			return self._config['connections'][connection][item_name]
		else:
			raise AttributeError("dbconfig has not item '%s'"%item_name)
	
	def _connection(self,conn_name):
		self._specific=conn_name
		return self

	def __getattr__(self,key):
		if key.upper()=='CONNECTION':
			return self._connection
		if self._specific==None:
			if key in self._config['connections'][self._default]:
				return self._get_specific_config_item(key,self._default)
			else:	
				raise AttributeError("Can't Find config item '%s'"%key)
		else:
			if key in self._config['connections'][self._specific]:
				res=self._get_specific_config_item(key,self._specific)
				self._specific=None
				return res
			else:
				raise AttributeError("Can't Find config item '%s'"%key)
class SessionConfigLoader(object):
	def __new__(cls,*args,**kw):
		pass
	def __init__(self):
		pass

class classproperty(object):
	def __init__(self,func):
		self._func=func
	def __get__(self,instance,owner_class):
		return self._func(owner_class)

class Config(dict):
	_config_loader={'database':DBConfigLoader()}
	def __init__(self):
		print("__init__ start")
	def __call__(self,*args,**kw):
		pass
	@classproperty
	def database(cls):
		return cls._config_loader.get('database')
	@classmethod
	def session(cls,key):
		if not instance(key,str):
			pass
	def __getattr__(cls,key):
		return 'not attribute found'

