# -*- coding:utf-8 -*-
import doctest

class ConfigLoader(object):
	def __init__(self,config):
		self._config=config
		self._default_driver_name=self._config.get('default')
		self._specific_driver_name=None
		self._all_drivers_name=self._config.get('drivers').keys()
	def _get_specific_driver_all_config_item(self,driver_name):
		if driver_name.lower() not in self._all_drivers_name:
			raise AttributeError(" %s config has no driver '%s'"%(self._config_name,driver_name.lower()))
		return self._config.get('drivers').get(driver_name.lower())
	def _get_specific_driver_config_item(self,item_name,driver_name):
		config=self._get_specific_driver_all_config_item(driver_name)
		if item_name.lower() not in config.keys():
			raise AttributeError(" %s config driver '%s' has no '%s' config item"%(self._config_name,driver_name,item_name))
		return config.get(item_name.lower())
	def _driver(self,driver_name,all_return=False):
		if all_return:
			return self._get_specific_driver_all_config_item(driver_name)
		self._specific_driver_name=None
		return self
	def __getattr__(self,key):
		if key.lower()=='driver':
			return self._driver
		if not self._specific_driver_name:
			if key.lower()=='all':
				return self._get_specific_driver_all_config_item(self._default_driver_name)	
			elif key.lower()=='driver_name':
				return self._default_driver_name
			else:
				return self._get_specific_driver_config_item(key,self._default_driver_name)
		else:
			if key.lower()=='all':
				config=self._get_specific_driver_all_config_item(self._specific_driver_name)
			elif key.lower()=='driver_name':
				config=self._specific_driver_name
			else:
				config=self._get_specific_driver_config_item(key,self._specific_driver_name)
			self._specific_driver_name=None
			return config
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
			raise AttributeError("database config has no connection %s"%connection.lower())
		if item_name in self._config['connections'][connection]:
			return self._config['connections'][connection][item_name]
		else:
			raise AttributeError("database connection has no such item '%s'"%item_name)
	def _get_specific_connection_all_config_item(self,connection):
		if connection.lower() not in self._all_connections:
			raise AttributeError("database config has no connection '%s'"%connection.lower())
		return self._config['connections'][connection]
	def _connection(self,conn_name,return_all=False):
		if return_all:
			return self._get_specific_connection_all_config_item(conn_name)
		self._specific_connection=conn_name.lower()
		return self
	def __getattr__(self,key):
		if key.upper()=='CONNECTION':
			return self._connection
		if not self._specific_connection:
			if key.lower()=='connection_name':
				return self._default_connection
			if key.lower()=='all':
				return self._get_specific_connection_all_config_item(self._default_connection)
			return self._get_specific_connection_config_item(key,self._default_connection)
		else:
			if key.lower()=='connection_name':
				conn_name=self._specific_connection
				self._specific_connection=None
				return conn_name
			item=self._get_specific_connection_config_item(key,self._specific_connection)
			self._specific_connection=None
			return item


class SessionConfigLoader(object):
	_all_drivers=('redis','file','mongo')
	def __new__(cls,*args,**kw):
		if not hasattr(cls,'_config_instance'):
			cls._config_instance=object.__new__(cls,*args,**kw)
		return cls._config_instance
	def __init__(self):
		self._config=__import__("conf",'app.conf').session
		self._default_driver=self._config.get('default')
		self._specific_driver=None
	def _get_specific_driver_config_item(self,item_name,driver_name):
		if driver_name.lower() not in self._all_drivers:
			raise AttributeError("session config has no driver '%s'"%(driver_name))
		if item_name in self._config['drivers'][driver_name]:
			return self._config['drivers'][driver_name].get(item_name)
		else:
			raise AttributeError("session driver %s has no such item '%s'"%(driver_name,item_name))
	def _get_specific_driver_all_config_item(self,driver_name):
		if driver_name.lower() not in self._all_drivers:
			raise AttributeError("session config has no driver '%s'"%(driver_name.lower()))
		return self._config['drivers'][driver_name.lower()]
	def _driver(self,driver_name,return_all=False):
		if return_all:
			return self._get_specific_driver_all_config_item(driver_name)
		self._specific_driver=driver_name.lower()
		return self
	def __getattr__(self,key):
		if key.upper()=='DRIVER':
			return self._driver
		if  not self._specific_driver:
			if key.lower()=='all':
				return self._get_specific_driver_all_config_item(self._default_driver)
			if key.lower()=='driver_name':
				return self._default_driver
			return self._get_specific_driver_config_item(key,self._default_driver)
		else:
			if key.lower()=='driver_name':
				driver_name=self._specific_driver
				self._specific_driver=None
				return driver_name
			item=self._get_specific_driver_config_item(key,self._specific_driver)
			self._specific_driver=None
			return item
class AuthConfigLoader(object):
	def __new__(cls,*args,**kw):
		if not hasattr(cls,'_config_instance'):
			cls._config_instance=object.__new__(cls,*args,**kw)
		return cls._config_instance
	def __init__(self):
		self._config=__import__("conf",'app.conf').authentication
	def __getattr__(self,key):
		if key not in self._config:
			raise AttributeError("authentication config has no such item '%s'"%(key))
		return self._config[key]
class AppConfigLoader(object):
	def __new__(cls,*args,**kw):
		if not hasattr(cls,'_config_insatnce'):
			cls._config_instance=object.__new__(cls,*args,**kw)
		return cls._config_instance
	def __init__(self):
		self._config=__import__("conf",'app.conf').app
	def __getattr__(self,key):
		if key not in self._config:
			raise AttributeError("app config has no such item '%s'"%key)
		return self._config.get(key)
class FileSystemConfigLoader(object):
	def __new__(cls,*args,**kw):
		if not hasattr(cls,'_config_instance'):
			cls._config_instance=object.__new__(cls,*args,**kw)
		return cls._config_instance
	def __init__(self):
		self._config=__import__("conf",locals(),globals()).filesystem
		self._default_driver=self._config.get('default')
		self._specific_driver=None
		self._all_drivers=self._config['drivers'].keys()
	def _get_specific_driver_config_item(self,item,driver_name):
		if driver_name.lower() not in  self._all_drivers:
			raise AttributeError("file system config has no such driver '%s'"%drive_rname.lower())
		if item.lower() not in self._config['drivers'][driver_name.lower()]:
			raise AttributeError("file system config driver '%s' has no such config item '%s'"%(driver_name.lower(),item.lower()))
		return self._config['drivers'][driver_name.lower()].get(item.lower())
	def _get_specific_driver_all_config_item(self,driver_name):
		if driver_name.lower() not in self._all_drivers:
			raise AttributeError("file system config has no such driver '%s'"%driver_name.lower())
		return self._config['drivers'].get(driver_name.lower())
	def _driver(self,driver_name,all_return=False):
		if all_return:
			return self._get_specific_driver_all_config_item(driver_name)
		self._specific_driver=driver_name.lower()
		return self
	def __getattr__(self,key):
		if key.lower()=='driver':
			self._driver
		if not self._specific_driver:
			if key.lower()=='all':
				return self._get_specific_driver_all_config_item(self._default_driver)
			if key.lower()=='driver_name':
				return self._default_driver
			return self._get_specific_driver_config_item(key,self._default_driver)
		else:
			if key.lower()=='driver_name':
				driver_name=self._specific_driver
				self._specific_driver=None
				return driver_name
			item=self._get_specific_driver_config_item(key,self._specific_driver)	
			self._specific_driver=None
			return item

class QueueConfigLoader(object):
	def __new__(cls,*args,**kw):
		if not hasattr(cls,'_config_instance'):
			cls._config_instance=object.__new__(cls,*args,**kw)	
		return cls._config_instance
	def __init__(self):
		self._config=__import__('conf',globals(),locals()).queue
		self._default_driver_name=self._config.get('default')
		self._specific_driver_name=None
		self._all_drivers_name=self._config['drivers'].keys()
	def _get_specific_driver_all_config_item(self,driver_name):
		if driver_name.lower() not in self._all_drivers_name:
			raise AttributeError(" queue config has no  '%s' driver "%(driver_name.lower()))
		return self._config.get('drivers').get(driver_name.lower())
	def _get_specific_driver_config_item(self,item_name,driver_name):
		config=self._get_specific_driver_all_config_item(driver_name)
		if item_name.lower() not in config:
			raise AttributeError("queue driver '%s' has no  '%s' config item"%(driver_name.lower(),item_name.lower()))
		return config.get(item_name.lower())
	def _driver(self,driver_name,all_return=False):
		if all_return:
			return self._get_specific_driver_all_config_item(driver_name)
		self._specific_driver_name=driver_name
		return self
	def __getattr__(self,key):
		if key.lower()=='driver':
			return self._driver
		if not self._specific_driver_name:
			if key.lower()=='all':
				return self._get_specific_driver_all_config_item(self._default_driver_name)
			elif key.lower()=='driver_name':
				return self._default_driver_name
			else:
				return self._get_specific_driver_config_item(key,self._default_driver_name)
		else:
			if key.lower()=='all':
				config=self._get_specific_driver_all_config_item(self._specific_driver_name)
			elif key.lower()=='driver_name':
				config=self._specific_driver_name
			else:
				config=self._get_specific_driver_config_item(key,self._specific_driver_name)
			self._specific_driver_name=None
			return config

class MailConfigLoader(ConfigLoader):
	def __new__(cls,*args,**kw):
		if not hasattr(cls,'_config_instance'):
			cls._config_instance=object.__new__(cls,*args,**kw)
		return cls._config_instance
	def __init__(self):
		config=__import__('conf',locals(),globals()).service['mail']
		self._config_name='mail'
		super(MailConfigLoader,self).__init__(config)
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
	_config_loader={'database':DBConfigLoader(),'session':SessionConfigLoader(),'authentication':AuthConfigLoader(),'app':AppConfigLoader(),'filesystem':FileSystemConfigLoader(),'queue':QueueConfigLoader(),'mail':MailConfigLoader()}
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
	@classproperty
	def app(cls):
		return cls._config_loader.get('app')
	@classproperty
	def filesystem(cls):
		return cls._config_loader.get('filesystem')
	@classproperty
	def queue(cls):
		return cls._config_loader.get('queue')
	@classproperty
	def mail(cls):
		return cls._config_loader.get('mail')
	def __getattr__(cls,key):
		return 'not attribute found'
if __name__=='__main__':
	'''doctest.testmod()'''
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
	r'''database testing code
	print(Config.database.all)
	print(Config.database.connection_name)
	print(Config.database.port)
	print(Config.database.connection('mysql').connection_name)
	print(Config.database.connection('mysql',True))
	print(Config.database.connection('mysql').port)
	print(Config.session.all)
	print(Config.session.driver_name)
	print(Config.session.expire)
	print(Config.session.driver('redis',True))
	print(Config.session.driver('redis').driver_name)
	print(Config.session.driver('redis').port)
	print(Config.app.template_path)
	'''
	r'''file system testing code
	print(Config.filesystem.access_key)
	print(Config.filesystem.secret_key)
	print(Config.filesystem.driver_name)
	print(Config.filesystem.all)
	'''
	#queue testing code
	#redis
	print(Config.queue.all)
	print(Config.queue.host)
	print(Config.queue.port)
	print(Config.queue.db)
	print(Config.queue.driver_name)
	#mysql
	print(Config.queue.driver('mysql',True))
	print(Config.queue.driver('mysql').all)
	print(Config.queue.driver('mysql').user)
	print(Config.queue.driver('mysql').host)
	print(Config.queue.driver('mysql').port)
	print(Config.queue.driver('mysql').password)
	print(Config.queue.driver('mysql').driver_name)
	#mongo
	print(Config.queue.driver('mongo',True))
	print(Config.queue.driver('mongo').all)
	print(Config.queue.driver('mongo').host)
	print(Config.queue.driver('mongo').port)
	print(Config.queue.driver('mongo').db)
	print(Config.queue.driver('mongo').driver_name)
	r'''
	#mail
	print(Config.mail.host)
	print(Config.mail.user)
	print(Config.mail.password)
	print(Config.mail.port)
	'''
