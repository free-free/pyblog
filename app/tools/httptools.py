#-*- coding:utf -*-


import functools
import inspect
import re
import logging
import json
logging.basicConfig(level=logging.INFO)
from   tools.log import Log
from   tools.session import SessionManager
from   tools.config import Config
import aiohttp.web
import os
try:
	import asyncio
except ImportError:
	logging.error("Can't Found Module asyncio")

try:
   import aiohttp
   from aiohttp import web
except ImportError:
	logging.error("Can't Found Module aiohttp")

class AppContainer(dict):
	def __init__(self,app,**kw):
		self._post=app['post']
		self._get=app['get']
		self._app=app
		self._cookie=app['cookie']
		self._app['set_cookie']=[]
		self._app['del_cookie']=[]
		self._app['response']=''
		self._app['redirect']=''
		self._config=Config
		super(AppContainer,self).__init__(**kw)
	def get_argument(self,name,default=None):
		if name not  in self._post and name not in self._get:
			return default
		if name in self._post:
			return self._post[name]
		if name in self._get:
			return self._get[name]
	def get_all_cookies(self):
		return self._cookie
	def get_cookie(self,cookie_name,default=None):
		if cookie_name in self._cookie:
			return self._cookie[cookie_name]
		return default
	def set_cookie(self,cookie_name,cookie_value,expire=None,*,domain=None,max_age=None,httponly=False,path='/'):
		self._app['set_cookie'].append({'cookie_name':cookie_name,'cookie_value':cookie_value,
'expire':expire,'domain':domain,'path':path,'max-age':max_age,'httponly':httponly})
	def clear_cookie(self,name,*,path='/',domain=None):
		self._app['del_cookie'].append({'cookie_name':name,'path':path,'domain':domain})

	def clear_all_cookies(self):
		if self._cookie:
			for ck in self._cookie:
				self.clear_cookie(ck)
	def render(self,content,**kw):
		if re.match('^[\w]+.html$',content):
			self._app['response']={'__template__':content,'parameter':kw}
		else:
			self._app['response']=content
	@property
	def session(self):
		if not hasattr(self,'_session_instance'):
			session_id=self.get_cookie('ssnid')
			if not session_id:
				session_id=self.get_argument("ssnid")
			if not session_id:
				self._session_instance=SessionManager(driver=self._config.session.driver_name,config=self._config.session.all)
			else:
				self._session_instance=SessionManager(session_id,driver=self._config.session.driver_name,config=self._config.session.all)
		return self._session_instance
	def session_end(self,expire=None):
		if hasattr(self,'_session_instance'):
			self.set_cookie('ssnid',self._session_instance.session_id)
			self._session_instance.save(expire)
	def session_destroy(self,session_id=None):
		if session_id:
			if not hasattr(self,'_session_instance'):
				self._session_instance=SessionManager(driver=self._config.session.driver_name,config=self._config.session.all)
			self._session_instance.delete(session_id)
		else:
			session_id=self.get_cookie("ssnid")
			if  session_id:
				self.clear_cookie('ssnid')
				if not hasattr(self,'_session_instance'):
					self._session_instance=SessionManager(driver=self._config.session.driver_name,config=self._config.session.all)
				self._session_instance.delete(session_id)
	def auth(self,auth=False):
		if auth:
			user_id=self.session[self._config.authentication.auth_id]
			if not user_id:
				self.redirect(self._config.authentication.login_url)
	def redirect(self,url):
		self._app['redirect']=url
class BaseHandler(object):
	r'''
			basic handler process url paramter
	
	'''
	def __init__(self,app,handlerfn):
		self._app=app
		self._handler=handlerfn
	def _param_generator(self,l):
		def _generator():
			for k in l:
				yield k
		return _generator
	@asyncio.coroutine
	def __call__(self,request):
		post=yield from request.post()
		get=request.GET
		cookie=request.cookies
		self._app['cookie']=request.cookies if request.cookies else {}
		self._app['get']=request.GET if request.GET else {}
		self._app['post']=post if post else {}
		container=AppContainer(app=self._app)
		container.auth(self._handler.__auth__)
		args=self._handler.__args__
		if len(args)==1:
			response=yield from self._handler(container)
		elif len(args)>1:
			param={}
			for k in args[1:]:
				if k not in request.match_info :
					raise NameError("Can't Found '%s'"%k)
				param[k]=request.match_info[k]
			param[self._handler.__args__[0]]=container
			response=yield from self._handler(**param)
		else:
			response=None
		return response



class Middleware(object):
	def response(app,handler):
		def check_set_cookie(res):
			if len(app['set_cookie'])>0:
				for k in app['set_cookie']:
					res.set_cookie(k['cookie_name'],k['cookie_value'],path=k['path'],expires=k['expire'],domain=k['domain'],httponly=k['httponly'])
			return res
		def check_del_cookie(res):
			if len(app['del_cookie'])>0:
				for k in app['del_cookie']:
					res.del_cookie(k['cookie_name'],path=k['path'],domain=k['domain'])
			return res
		@asyncio.coroutine
		def _response(request):
			res=yield from handler(request)
			res=res if res else app.get('response')
			if app.get('redirect'):
				redirect_url=app.get('redirect')
				app['redirect']=''
				res= aiohttp.web.HTTPFound(redirect_url)
				check_set_cookie(res)
				check_del_cookie(res)
				return res
			if isinstance(res,web.StreamResponse):
				res=res
			elif isinstance(res,bytes):
				res=web.Response(body=res)
				res.content_type='application/octet-stream'
			elif isinstance(res,str):
				res=web.Response(body=res.encode("utf-8"))
				res.content_type='text/html;charset=utf-8'
			elif isinstance(res,dict):
				template=res.get('__template__')
				if template is None:
					res=web.Response(body=json.dumps(res,ensure_ascii=False,default=lambda x:x.__dict__).encode("utf-8"))
					res.content_type='application/json;charset=utf-8'
				else:
					res=web.Response(body=app['__templating__'].get_template(template).render(**res['parameter']).encode("utf-8"))
					res.content_type='text/html;charset=utf-8'
			else:
				res=res
			res=check_set_cookie(res)
			res=check_del_cookie(res)
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
	_none_variable_routes=list()
	_incomplete_variable_routes=list()
	_complete_variable_routes=list()
	def __init__(self):
		pass
	@classmethod
	def add_routes(cls,wrapper):
		if wrapper.__url__.count('{')!=0:
			if wrapper.__url__.endswith('/'):
				wrapper.__url__=wrapper.__url__[:wrapper.__url__.rindex('/')]
			if wrapper.__url__.count('{')<wrapper.__url__.count('/'):
				Route._incomplete_variable_routes.append(wrapper)
			else:
				Route._complete_variable_routes.append(wrapper)
		else:
			Route._none_variable_routes.append(wrapper)
	@classmethod
	def get(cls,url,*,auth=False):
		def decorator(func):
			@functools.wraps(func)
			def wrapper(*args,**kw):
				return func(*args,**kw)
			wrapper.__method__='GET'
			wrapper.__url__=url
			wrapper.__auth__=auth
			wrapper.__args__=inspect.getargspec(func)[0]
			cls.add_routes(wrapper)
			return wrapper
		return decorator
	@classmethod
	def post(cls,url,*,auth=False):
		def decorator(func):
			@functools.wraps(func)
			def wrapper(*args,**kw):
				return func(*args,**kw)
			wrapper.__method__='POST'
			wrapper.__url__=url
			wrapper.__auth__=auth
			wrapper.__args__=inspect.getargspec(func)[0]
			cls.add_routes(wrapper)
			return wrapper
		return decorator
	@classmethod
	def put(cls,url,*,auth=False):
		def decorator(func):
			@functools.wraps(func)
			def wrapper(*args,**kw):
				return func(*args,**kw)
			wrapper.__method__='PUT'
			wrapper.__url__=url
			wrapper.__auth__=auth
			wrapper.__args__=inspect.getargspec(func)[0]
			cls.add_routes(wrapper)
			return wrapper
		return decorator
	@classmethod
	def delete(cls,url,*,auth=False):
		def decorator(func):
			@functools.wraps(func)
			def wrapper(*args,**kw):
				return func(*args,**kw)
			wrapper.__method__='DELETE'
			wrapper.__url__=url
			wrapper.__auth__=auth
			wrapper.__args__=inspect.getargspec(func)[0]
			cls.add_routes(wrapper)
			return wrapper
		return decorator
	@classmethod
	def sort_variable_routes(cls,routes):
		route_length=len(routes)
		i=0
		while i<route_length:
			j=i
			while j>0 and routes[j].__url__.count('{')<routes[j-1].__url__.count('{'):
				swap=routes[j]
				routes[j]=routes[j-1]
				routes[j-1]=swap
				j-=1
			i+=1
		return routes
	@classmethod
	def sort_none_variable_routes(cls,routes):
		route_length=len(routes)
		i=0
		while i<route_length:
			j=i
			while j>0 and routes[j].__url__.count('/')<=routes[j-1].__url__.count('/'):
				if routes[j].__url__.count('/')<routes[j-1].__url__.count('/'):
					swap=routes[j]
					routes[j]=routes[j-1]
					routes[j-1]=swap
				else:
					if len(routes[j].__url__)<len(routes[j-1].__url__):
						swap=routes[j]
						routes[j]=routes[j-1]
						routes[j-1]=swap
				j-=1
			i+=1
		return routes
	
	@classmethod
	def process_routes(cls,app,routes):
		for handler in routes:
			_method=getattr(handler,'__method__',None)
			_path=getattr(handler,'__url__',None)
			if _path is None or _method is None:
				raise ValueError("__method__ or __url__ not define in %s."%str(handler.__name__))
			if not asyncio.iscoroutinefunction(handler) and not inspect.isgeneratorfunction(handler):
				handler=asyncio.coroutine(handler)
			if len(_path)>1 and _path.endswith('/'):
				app.router.add_route(_method,_path.rsplit('/',1)[0],BaseHandler(app,handler))
				app.router.add_route(_method,_path,BaseHandler(app,handler))
			elif not _path.endswith('/'):
				app.router.add_route(_method,_path,BaseHandler(app,handler))
				app.router.add_route(_method,_path+'/',BaseHandler(app,handler))
			else:
				app.router.add_route(_method,_path,BaseHandler(app,handler))
	@classmethod
	def register_route(cls,app):
		Route._none_variable_routes=cls.sort_none_variable_routes(Route._none_variable_routes)
		cls.process_routes(app,Route._none_variable_routes)
		Route._incomplete_variable_routes=cls.sort_variable_routes(Route._incomplete_variable_routes)
		cls.process_routes(app,Route._incomplete_variable_routes)
		Route._complete_variable_routes=cls.sort_variable_routes(Route._complete_variable_routes)
		cls.process_routes(app,Route._complete_variable_routes)	
		app.router.add_static(Config.app.static_prefix,os.path.join(os.path.dirname(os.path.dirname(__file__)),Config.app.static_path))
if __name__=='__main__':
	@Route.get('/uer/profile')
	def user_profile(name):
		print(name)
	@Route.post('/usr/gallery')
	def user_gallery(name):
		print(name)
	#Route.register_route()
	#Route.register_route()
