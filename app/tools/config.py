# -*- coding:utf-8 -*-
		
class Config(dict):
	conf=__import__('conf','app.conf')
	def __init__(self):
		pass
	def __call__(self,*args,**kw):
		pass
	@classmethod
	def database(cls,*key):
		if len(key)==1:
			if not isinstance(key[0],str):
				raise TypeError("config key must be str")
			default=Config.conf.database['default']
			if not isinstance(default,str):
				raise TypeError
			return Config.conf.database['connections'][default][key]
		elif len(key)==2:
			if not isinstance(key[0],str) or not isinstance(key[1],str):
				raise Type("Config key must be str")
			return Config.conf.database['connections'][key[0]][key[1]]
		else:
			raise Exception
	@classmethod
	def session(cls,key):
		if not instance(key,str):
			pass
	def __getattr__(cls,key):
		return 'not attribute found'

