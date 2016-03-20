# -*- coding:utf-8 -*-
import doctest

class DBConfigLoader(object):
	_config_instance=None
	_all_connections=('mysql','mongodb')
	def __new__(cls,*args,**kw):
		if cls._config_instance==None:
			cls._config_instance=object.__new__(cls,*args,**kw)
		return cls._config_instance
	def __init__(self):
		self._config=__import__('conf','app.conf').database
		self._default_connection=self._config['default']
		self._specific_connection=None
	def _get_specific_connection_config_item(self,item_name,connection):
		if connection.lower() not in self._all_connections:
			raise AttributeError("database config has not connection %s"%connection.lower())
		if item_name in self._config['connections'][connection]:
			return self._config['connections'][connection][item_name]
		else:
			raise AttributeError("database connection has not such item '%s'"%item_name)
	def _connection(self,conn_name):
		self._specific_connection=conn_name.lower()
		return self

	def __getattr__(self,key):
		if key.upper()=='CONNECTION':
			return self._connection
		if not self._specific_connection:
			return self._get_specific_connection_config_item(key,self._default_connection)
		else:
			return self._get_specific_connection_config_item(key,self._specific_connection)
class SessionConfigLoader(object):
	_all_drivers=('redis','file','mongo')
	def __new__(cls,*args,**kw):
		if not hasattr(cls,'_config_instance'):
			cls._config_instance=object.__new__(cls,*args,**kw)
		return cls._config_instance
	def __init__(self):
		self._config=__import__("conf",'app.confg').session
		self._default_driver=self._config.get('default')
		self._specific_driver=None
	def _get_specific_driver_config_item(self,item_name,driver_name):
		if driver_name.lower() not in self._all_drivers:
			raise AttributeError("session config has no driver '%s'"%(driver_name))
		if item_name in self._config['drivers'][driver_name]:
			return self._config['drivers'][driver_name].get(item_name)
		else:
			raise AttributeError("session driver %s has no such item '%s'"%(driver_name,item_name))
	def _driver(self,driver_name):
		self._specific_driver=driver_name.lower()
		return self
	def __getattr__(self,key):
		if key.upper()=='DRIVER':
			return self._driver
		if  not self._specific_driver:
			return self._get_specific_driver_config_item(key,self._default_driver)
		else:
			return self._get_specific_driver_config_item(key,self._specific_driver)
class AuthConfigLoader(object):
	def __new__(cls,*args,**kw):
		if not hasattr(cls,'_config_instance'):
			cls._config_instance=object.__new__(cls,*args,**kw)
		return cls._config_instance
	def __init__(self):
		self._config=__import__("conf",'app.config').authentication
	def __getattr__(self,key):
		if key not in self._config:
			raise AttributeError("authentication config has no such item '%s'"%(key))
		return self._config[key]
class classproperty(object):
	def __init__(self,func):
		self._func=func
	def __get__(self,instance,owner_class):
		return self._func(owner_class)

class Config(dict):
	r'''
	>>> Config.session.session_dir
	'/tmp/session/'
	>>> Config.session.expire_file
	'session_expire'
	>>> Config.session.driver('redis').host
	'localhost'
	>>> Config.session.driver('redis').port
	6379
	>>> Config.session.driver('mongo').port
	27017
	>>> Config.session.driver('mongo').host
	'localhost'
	>>> Config.database.port
	3306
	>>> Config.database.connection('mongodb').port
	27017
	'''
	_config_loader={'database':DBConfigLoader(),'session':SessionConfigLoader(),'authentication':AuthConfigLoader()}
	def __init__(self):
		print("__init__ start")
	def __call__(self,*args,**kw):
		pass
	@classproperty
	def database(cls):
		return cls._config_loader.get('database')
	@classproperty
	def session(cls):
		return cls._config_loader.get('session')
	@classproperty
	def authentication(cls):
		return cls._config_loader.get('authentication')
	def __getattr__(cls,key):
		return 'not attribute found'
if __name__=='__main__':
	doctest.testmod()
	r'''
	print(Config.session.session_dir)
	print(Config.session.expire_file)
	print(Config.session.expire)
	print(Config.session.driver('redis').host)
	print(Config.session.driver('redis').port)	
	print(Config.session.driver('redis').db)
	print(Config.session.driver('redis').expire)
	print(Config.session.driver('mongo').host)
	print(Config.session.driver('mongo').port)
	print(Config.session.driver('mongo').db)
	print(Config.session.driver('mongo').expire)
	print(Config.database.port)
	print(Config.database.password)
	print(Config.database.connection('mongodb').port)
	print(Config.authentication.auth_table)
	print(Config.authentication.auth_id)
	print(Config.authentication.login_url)
	'''
