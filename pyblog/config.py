# -*- coding:utf-8 -*-
import doctest
import sys
class ConfigError(Exception):
	pass
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
		self._config=__import__('conf',globals(),locals()).database
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
		self._config=__import__("conf",locals(),globals()).session
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
		self._config=__import__("conf",locals(),globals()).app
	def __getattr__(self,key):
		if key not in self._config:
			raise AttributeError("app config has no such item '%s'"%key)
		return self._config.get(key)
class StorageConfigLoader(object):
	#__slots__=('__config','__default_disk','__default_disk_name','__specific_disk','__specific_disk_name','__all_disks')
	def __new__(cls,*args,**kw):
		if not hasattr(cls,'_config_instance'):
			cls._config_instance=object.__new__(cls,*args,**kw)
		return cls._config_instance
	def __init__(self):
		super(StorageConfigLoader,self).__init__()
		self.__config=__import__("conf",locals(),globals()).storage
		self.__default_disk=self.__config['disks'].get(self.__config.get('default'))
		self.__default_disk_name=self.__config.get("default")
		self.__specific_disk=None
		self.__specific_disk_name=None
		self.__all_disks=self.__config['disks']
	def _get_disk_config(self,item,disk):
		if disk.lower() not in  self.__all_disks:
			raise AttributeError("storage config has no such driver '%s'"%disk.lower())
		if item.lower() not in self.__all_disks[disk.lower()]:
			raise AttributeError("storage config driver '%s' has no such config item '%s'"%(disk.lower(),item.lower()))
		return self.__all_disks[disk.lower()].get(item.lower())
	def _get_disk_all_config(self,disk):
		if disk.lower() not in self.__all_disks:
			raise AttributeError("storage config has no such driver '%s'"%disk.lower())
		return self.__all_disks.get(disk.lower())
	def _disk(self,disk):
		self.__specific_disk=self._get_disk_all_config(disk)
		self.__specific_disk_name=disk
		return self
	def __getattr__(self,key):
		if key.lower()=='disk':
			return self._disk
		if not self.__specific_disk:
			if key.lower()=='all':
				return self.__default_disk
			if key.lower()=='disk_name':
				return self.__default_disk_name
			return self._get_disk_config(key,self.__default_disk_name)
		else:
			if key.lower()=='all':
				all_config=self.__specific_disk
				self.__specific_disk=None
				self.__specific_disk_name=None
				return all_config
			if key.lower()=='disk_name':
				disk_name=self.__specific_disk_name
				self.__specific_disk=None
				self.__specific_disk_name=None
				return disk_name
			item=self._get_disk_config(key,self.__specific_disk_name)	
			self.__specific_disk=None
			self.__specific_disk_name=None
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
		if key.lower() in self.__config:
			return self.__config[key.lower()]
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
class CacheConfigLoader(object):
	def __new__(cls,*args,**kw):
		if not hasattr(cls,'_config_instance'):
			cls._config_instance=object.__new__(cls,*args,**kw)
		return cls._config_instance
	def __init__(self):
		__import__('conf',locals(),globals())
		mod=sys.modules['conf']
		self._config=mod.cache
		self._default_driver_name=self._config.get("default")
		self._default_driver=self._config.get("drivers").get(self._default_driver_name)
		self._all_drivers=self._config.get("drivers")
		self._specific_driver=None
		self._specific_driver_name=None
	def _get_driver_all_config(self,driver_name):
		if driver_name not in self._all_drivers:
			raise ConfigError("no cache driver '%s' config"%(driver_name))
		return self._all_drivers[driver_name]
	def _get_driver_config(self,item,driver_name):
		config=self._get_driver_all_config(driver_name)
		if item not in config:
			raise ConfigError("cache driver '%s' has no config item '%s'"%(driver_name,item))
		return config.get(item)
	def _driver(self,driver_name):
		self._specific_driver_name=driver_name
		self._specific_driver=self._get_driver_all_config(driver_name)
		return self
	def __getattr__(self,key):
		if key=='driver':
			return self._driver
		elif not  self._specific_driver:
			if key=='all':
				return self._default_driver
			elif key=='driver_name':
				return self._default_driver_name
			else:
				return self._get_driver_config(key,self._default_driver_name)
		else:
			if key=='all':
				ret=self._specific_driver
				self._specific_driver=None
				self._specific_drivr_name=None
				return ret
			elif key=='driver_name':
				ret=self._specific_driver_name	
				self._specific_driver_name=None
				self._specific_driver=None
				ret
			else:
				ret=self._get_driver_config(key,self._specific_driver_name)
				self._specific_driver_name=None
				self._specific_driver=None
				return ret
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
	def __init__(self):
		pass
	def __call__(self,*args,**kw):
		pass
	@classproperty
	def database(cls):
		if not hasattr(cls,'__database'):
			cls.__database=DBConfigLoader()
		return cls.__database
	@classproperty
	def session(cls):
		if not hasattr(cls,'__session'):
			cls.__session=SessionConfigLoader()
		return cls.__session
	@classproperty
	def authentication(cls):
		if not hasattr(cls,'__auth'):
			cls.__auth=AuthConfigLoader()
		return cls.__auth
	@classproperty
	def app(cls):
		if not hasattr(cls,'__app'):
			cls.__app=AppConfigLoader()
		return cls.__app
	@classproperty
	def storage(cls):
		if not hasattr(cls,'__storage'):
			cls.__storage=StorageConfigLoader()
		return cls.__storage
	@classproperty
	def queue(cls):
		if not hasattr(cls,'__queue'):
			cls.__queue=QueueConfigLoader()
		return cls.__queue
	@classproperty
	def mail(cls):
		if not hasattr(cls,'__mail'):
			cls.__mail=MailConfigLoader()
		return cls.__mail
	@classproperty
	def cache(cls):
		if not hasattr(cls,'__cache'):
			cls.__cache=CacheConfigLoader()
		return cls.__cache
	def __getattr__(cls,key):
		return 'not attribute found'
if __name__=='__main__':
	pass

