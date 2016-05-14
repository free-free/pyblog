#-*- coding:utf-8 -*-
from memcache_cache import MemcacheCache
from redis_cache import RedisCache


class CacheFactory(object):
	def __new__(cls,*args,**kw):
		assert len(args)==2,"args must be 'driver' and 'config'"
		assert isinstance(args[0],str)
		assert isinstance(args[1],dict)
		cls.__driver=args[0]
		cls.__config=args[1]
		return cls._resolve_cache_driver(cls.__driver,cls.__config)
	@classmethod
	def _resolve_cache_driver(cls,driver,config):
		if driver.lower()=='redis':
			return cls._resolve_redis_cache(config)
		elif driver.lower()=='memcache':
			return cls._resolve_memcache_cache(config)
	@classmethod
	def _resolve_redis_cache(cls,config):
		return RedisCache(config.get("host"),config.get("port"),config.get("db"))
	@classmethod
	def _resolve_memcache_cache(cls,config):
		return MemcacheCache(config.get("host"),config.get("port"))


if __name__=='__main__':
	pass
	#rds=CacheFactory('redis',{'host':'127.0.0.1','port':6379,'db':0})
	#mem=CacheFactory("memcache",{"host":"127.0.0.1",'port':11211})
	#rds.put("name","huangbiao")
	#print(rds.get("name"))
	#mem.put("name","xiaoming")
	#print(mem.get("name"))

	
