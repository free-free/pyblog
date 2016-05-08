#-*- coding:utf-8 -*-
import logging
logging.basicConfig(level=logging.ERROR)
from cache_abstract import CacheAbstractDriver
try:
	import memcache
except ImportError:
	logging.error("Can't import 'memcache' module")
	exit(-1)

class MemcacheCache(CacheAbstractDriver):
	def __init__(self,servers):
		assert isinstance(servers,list)
		self.__client=memcache.Client(servers)
