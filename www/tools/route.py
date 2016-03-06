#-*- coding:utf -*-


import functools


class Route(object):
	_routes=set()
	def __init__(self):
		pass
	@classmethod
	def get(cls,url):
		def decorator(func):
			@functools.wraps(func):
			def wrapper(*args,**kw):
				return func(*args,**kw)
			wrapper.__method__='GET'
			wrapper.__url__=url
			Route._routes.add(wrapper)
			return wrapper
		return decorator
	@classmethod
	def post(cls,url):
		def decorator(func):
			@functools.wraps(func):
			def wrapper(*args,**kw):
				return func(*args,**kw)
			wrapper.__method__='POST'
			wrapper.__url__=url
			Route._routes.add(wrapper)
			return wrapper
		return decorator
	@classmethod
	def put(cls,url):
		def decorator(func):
			@functools.wraps(func):
			def wrapper(*args,**kw):
				return func(*args,**kw)
			wrapper.__method__='PUT'
			wrapper.__url__=url
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
			Route._routes.add(wrapper)
			return wrapper
		return decorator
	@classmethod
	def register_route(cls,app):
		for handler in Route._routes:
			app.router.add_route(handler.__method__,handler.__url__,handler)

