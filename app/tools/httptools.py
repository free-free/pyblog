#-*- coding:utf -*-


import functools
import inspect
import logging
logging.basicConfig(level=logging.INFO)
from   .log import Log
try:
	import asyncio
except ImportError:
	logging.error("Can't Found Module asyncio")

try:
   import aiohttp
   from aiohttp import web
except ImportError:
	logging.error("Can't Found Module aiohttp")


class BaseHandler(object):
	r'''
			basic handler process url paramter
	
	'''
	def __init__(self,handlerfn):
		self._handler=handlerfn
	def _param_generator(self,l):
		def _generator():
			for k in l:
				yield k
		return _generator
	@asyncio.coroutine
	def __call__(self,request):
		print(request)
		params={}
		for k,v in request.match_info.items():
			params[k]=v
		args=self._handler.__args__
		if len(args)==0:
			response=yield from self._handler()
		else:
			param={}
			print(request)
			for k in args:
				if k not in params:
					raise NameError("Can't Found '%s'"%k)
				param[k]=params[k]
			response=yield from self._handler(**param)
		return response

class Middleware(object):
	def response(app,handler):
		@asyncio.coroutine
		def _response(request):
			res=yield from handler(request)
			if isinstance(res,web.StreamResponse):
				return res
			elif isinstance(res,bytes):
				res=web.Response(body=res)
				res.content_type='application/octet-stream'
				return res
			elif isinstance(res,str):
				res=web.Response(body=res.encode("utf-8"))
				res.content_type='text/html;charset=utf-8'
				return res
			elif isinstance(res,dict):
				template=res.get('__template__')
				if template is None:
					res=web.Response(body=json.dumps(res,ensure_ascii=False,default=lambda x:x.__dict__).encode("utf-8"))
					res.content_type='application/json;charset=utf-8'
					return res
				else:
					res=web.Response(body=app['__templating__'].get_template(template).render(**res).encode("utf-8"))
					res.content_type='text/html;charset=utf-8'
					return res
			else:
				return res
		return _response
	def log(app,handler):
		@asyncio.coroutine
		def _log(request):
			Log.info("%s:%s===>%s"%(request.host,request.method,request))
			return (yield from handler(request))
		return _log
	@classmethod
	def allmiddlewares(cls):
		middlewares=list()
		for k,v in cls.__dict__.items():
			if k.startswith('__') and k.endswith('__') or k=='allmiddlewares':
				continue
			if not asyncio.iscoroutinefunction(v):
				v=asyncio.coroutine(v)
			middlewares.append(v)
		return middlewares
class Route(object):
	r'''
		Route class is responsible for routes adding and routes registering to  aiohttp
	'''
	_routes=set()
	def __init__(self):
		pass
	@classmethod
	def get(cls,url):
		def decorator(func):
			@functools.wraps(func)
			def wrapper(*args,**kw):
				return func(*args,**kw)
			wrapper.__method__='GET'
			wrapper.__url__=url
			wrapper.__args__=inspect.getargspec(func)[0]
			Route._routes.add(wrapper)
			return wrapper
		return decorator
	@classmethod
	def post(cls,url):
		def decorator(func):
			@functools.wraps(func)
			def wrapper(*args,**kw):
				return func(*args,**kw)
			wrapper.__method__='POST'
			wrapper.__url__=url
			wrapper.__args__=inspect.getargspec(func)[0]
			Route._routes.add(wrapper)
			return wrapper
		return decorator
	@classmethod
	def put(cls,url):
		def decorator(func):
			@functools.wraps(func)
			def wrapper(*args,**kw):
				return func(*args,**kw)
			wrapper.__method__='PUT'
			wrapper.__url__=url
			wrapper.__args__=inspect.getargspec(func)[0]
			Route._routes.add(wrapper)
			return wrapper
		return decorator
	@classmethod
	def delete(cls,url):
		def decorator(func):
			@functools.wraps(func)
			def wrapper(*args,**kw):
				return func(*args,**kw)
			wrapper.__method__='DELETE'
			wrapper.__url__=url
			wrapper.__args__=inspect.getargspec(func)[0]
			Route._routes.add(wrapper)
			return wrapper
		return decorator
	@classmethod
	def register_route(cls,app):
		for handler in Route._routes:
			_method=getattr(handler,'__method__',None)
			_path=getattr(handler,'__url__',None)
			if _path is None or _method is None:
				raise ValueError('_path or _method not defined in %s.'%str(handler))
			if not asyncio.iscoroutinefunction(handler) and not inspect.isgeneratorfunction(handler):
				handler=asyncio.coroutine(handler)
			app.router.add_route(_method,_path,BaseHandler(handler))
			#handler('Jell')
			#print(handler.__method__)
			#print(handler.__url__)
if __name__=='__main__':
	@Route.get('/uer/profile')
	def user_profile(name):
		print(name)
	@Route.post('/usr/gallery')
	def user_gallery(name):
		print(name)
	Route.register_route()
	Route.register_route()
