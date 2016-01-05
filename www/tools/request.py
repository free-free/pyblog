#!/usr/bin/env python3
import functools
import asyncio
try:
	import aiohttp
except:
	raise ImportError("'aiohttp' module not found")

def get(path):
	def get_decorator(func):
		@functools.wraps(func)
		def wrapper(*args,**kw):
			return func(*args,**kw)
		wrapper.__method__='GET'
		wrapper.__route__=path
		return wrapper
	return get_decorator
def post(path):
	def post_decorator(func):
		@functools.wraps(func)
		def wrapper(*args,**kw):
			return func(*args,**kw)
		wrapper.__method__='POST'
		wrapper.__route__=path
		return wrapper
	return post_decorator
def add_router(app,fn):
	method=getattr(fn,'__method__',None)
	path=getattr(fn,'__route__',None)
	if path is None or method is None:
		raise ValueError('@get or @post not defined in %s.'%str(fn))
	if not asyncio.iscoroutinefunction(fn) and not inspect.isgeneratorfunction(fn):
		fn=asyncio.coroutine(fn)
	app.router.add_route(method,path,request_handler(app,fn))

class request_handler(object):
	def __init__(self,app,fn):
		self._app=app
		self._func=fn
	@asyncio.coroutine
	def __call__(self,request):
		response=yield from self._func(**kw)
		return response


