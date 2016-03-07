# -*- coding:utf-8 -*-

class Config(dict):
	conf=__import__('conf','app.conf')
	def __init__(self):
		pass
	def __call__(self,*args,**kw):
		pass
	@classmethod
	def database(cls,key):
		if not isinstance(key,str):
			raise TypeError("config key must be str")
		default=Config.conf.database['default']
		if not isinstance(default,str):
			raise TypeError
		return Config.conf.database['connections'][default][key]
	@classmethod
	def session(cls,key):
		if not instance(key,str):
			pass
	def __getattr__(cls,key):
		return 'not attribute found'

