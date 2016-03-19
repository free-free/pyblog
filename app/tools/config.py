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
				return self._get_specific_config_item(key,self._specific)
			else:
				raise AttributeError("Can't find config item '%s'"%key)
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
		if  self._specific_driver==None:
			return self._get_specific_driver_config_item(key,self._default_driver)
		else:
			return self._get_specific_driver_config_item(key,self._specific_driver)

class classproperty(object):
	def __init__(self,func):
		self._func=func
	def __get__(self,instance,owner_class):
		return self._func(owner_class)

class Config(dict):
	_config_loader={'database':DBConfigLoader(),'session':SessionConfigLoader()}
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
	def __getattr__(cls,key):
		return 'not attribute found'
if __name__=='__main__':
	#print(Config.session.session_dir)
	#print(Config.session.expire_file)
	#print(Config.session.expire)
	#print(Config.session.driver('redis').host)
	#print(Config.session.driver('redis').port)	
	#print(Config.session.driver('redis').db)
	#print(Config.session.driver('redis').expire)
	#print(Config.session.driver('mongo').host)
	#print(Config.session.driver('mongo').port)
	#print(Config.session.driver('mongo').db)
	#print(Config.session.driver('mongo').expire)
	print(Config.database.port)
