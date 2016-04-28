#-*- coding:utf-8 -*-


import functools
import inspect
import re
import hashlib
import hmac
import logging
import json
logging.basicConfig(level=logging.INFO)
from   tools.log import Log
from   tools.session import SessionManager
from   tools.config import Config
import os
try:
	import asyncio
except ImportError:
	logging.error("Can't Found Module asyncio")
	exit()
try:
	import aiohttp
	import aiohttp.web
	import aiohttp.errors
	from aiohttp import web
except ImportError:
	logging.error("Can't Found Module aiohttp")
	exit()
try:
	import jinja2
except ImportError:
	logging.error("can't import 'jinja2' module")
	exit()

HTTP_ERROR_REASON_EN={
			400:"Bad Request",
			401:"Unauthorized",
			402:"Payment Required",
			403:"Forbidden",
			404:"Page Not Found",
			405:"Bad Request",
			406:"Not Acceptable",
			407:"Proxy Authentication Required",
			408:"Request Timeed-Out",
			409:"Conflict",
			500:"Server Internal Error",
			501:"Not Implemented",
			502:"Bad Gateway",
			503:"Server Unavailable",
			504:"Gatewy Time-Out",
			505:"HTTP Version Not Supported"
		}
DEFAULT_HTTP_ERROR_PAGE="""
					<!DOCTYPE HTML>
					<html><head><title>%s</title><style>	
							.error-box{
								height:inherit;
								width:inherit;
							}
							.error{
								display:block;
								width:inherit;
							}
							.title{
								color:#efefef;
								font-size:100px;
								height:200px;
								line-height:200px;
								text-align:center;
								letter-spacing:10px;
								font-weight:1;
							}
							.code{
								color:#999;
								font-size:48px;
								text-align:center;
								height:400px;
								font-weight:100;
								line-height:200px;
							}
							</style>
						</head>
						<body>
							<div class="error-box">
								<span class="error title">	
									%s
								</span>
								<span class="error code">%s %s</span>
						</div></body></html>"""
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
		self._app['status']=''
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
	def session_end(self,expire=None,*,auth=False):
		if hasattr(self,'_session_instance'):
			if auth:
				m=hmac.new(str(self._session_instance[Config.authentication.auth_id]).encode("utf-8"),self._session_instance.session_id.encode("utf-8"),hashlib.sha1)
				auth_unss=m.hexdigest()
				self._session_instance['auth_unss']=auth_unss
				self.set_cookie('unss',auth_unss)
			self._session_instance.save(expire)
			self.set_cookie('ssnid',self._session_instance.session_id)
			return self._session_instance.session_id
		return None
	def session_destroy(self,session_id=None):
		if session_id:
			if not hasattr(self,'_session_instance'):
				self._session_instance=SessionManager(driver=self._config.session.driver_name,config=self._config.session.all)
			self._session_instance.delete(session_id)
		else:
			session_id=self.get_cookie("ssnid")
			if  session_id:
				self.clear_cookie('ssnid')
				self.clear_cookie('unss')
				if not hasattr(self,'_session_instance'):
					self._session_instance=SessionManager(driver=self._config.session.driver_name,config=self._config.session.all)
				self._session_instance.delete(session_id)
		return session_id
	def redirect(self,url):
		self._app['redirect']=url
	def set_status(self,code,*,message=None):
		assert isinstance(code,int)
		if message:
			self._app['status']={'code':code,'message':message}
		else:
			error_template='errors/'+str(code)+'.html'
			try:
				error_page=self._app['__templating__'].get_template(error_template).render()
			except jinja2.exceptions.TemplateNotFound:
				error_page=(DEFAULT_HTTP_ERROR_PAGE%(code,"Pyblog 1.0",code,HTTP_ERROR_REASON_EN.get(code)))
			self._app['status']={'code':code,'message':error_page}
class BaseHandler(object):
	r'''
			basic handler process url paramter
	
	#'''
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
		self._app_container=AppContainer(app=self._app)
		args=self._handler.__args__
		if len(args)<=1:
			response=yield from self._handler(self._app_container)
		elif len(args)>1:
			param={}
			for k in args[1:]:
				if k not in request.match_info :
					raise NameError("Can't Found '%s'"%k)
				param[k]=request.match_info[k]
			param[self._handler.__args__[0]]=self._app_container
			response=yield from self._handler(**param)
		return response

class Middleware(object):
	def http_error_middleware(app,handler):
		@asyncio.coroutine
		def _handler(request):
			try:
				res=yield from handler(request)
			except web.HTTPClientError as e:	
				try:
					error_template='errors/'+str(e.status_code)+'.html'
					error_page=app.get('__templating__').get_template(error_template).render()
				except jinja2.exceptions.TemplateNotFound:
					error_page=DEFAULT_HTTP_ERROR_PAGE%(e.status_code,"Pyblog 1.0",e.status_code,e.reason)
				res=web.Response(status=e.status_code,body=error_page.encode("utf-8"))
			except web.HTTPServerError as e:
				try:
					error_template='errors/'+str(e.status_code)+'.html'
					error_page=app.get('__templating__').get_template(error_template).render()
				except jinja2.exceptions.TemplateNotFound:
					error_page=DEFAULT_HTTP_ERROR_PAGE%(e.status_code,"Pyblog 1.0",e.status_code,e.reason)
				res=web.Response(status=e.status_code,body=error_page.encode("utf-8"))
			except Exception as e:
				error_page=DEFAULT_HTTP_ERROR_PAGE%(500,"Pyblog 1.0",500,"Server Internal Error")				
				Log.error(e)
				res=web.Response(status=500,body=error_page.encode('utf-8'))
			else:
				if app.get('status'):
					res=web.Response(status=app.get('status').get('code'),body=app.get('status').get('message').encode('utf-8'))
					return res
			return res
		return _handler
	def cookie_middleware(app,handler):
		@asyncio.coroutine
		def _cookie(request):
			res=yield from handler(request)
			if app.get('set_cookie') and len(app['set_cookie'])>0:
				for k in app['set_cookie']:
					res.set_cookie(k['cookie_name'],k['cookie_value'],path=k['path'],expires=k['expire'],domain=k['domain'],httponly=k['httponly'])		
			if app.get('del_cookie') and len(app['del_cookie'])>0:
				for k in app['del_cookie']:
					res.del_cookie(k['cookie_name'],path=k['path'],domain=k['domain'])
			return res
		return _cookie
	def response_middleware(app,handler):
		@asyncio.coroutine
		def _response(request):
			res=yield from handler(request)
			res=app.get('response') if app.get('response') else res
			if app.get('redirect'):
				redirect_url=app.get('redirect')
				app['redirect']=''
				res= aiohttp.web.HTTPFound(redirect_url)
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
			return res
		return _response
	def log_middleware(app,handler):
		@asyncio.coroutine
		def _log(request):
			Log.info("%s:%s===>%s"%(request.host,request.method,request))
			return (yield from handler(request))
		return _log
	def auth_middleware(app,handler):
		@asyncio.coroutine
		def _auth(request):
			if hasattr(request.match_info.handler,'_handler'):
				matched_handler=request.match_info.handler._handler
				if matched_handler.__auth__:
					session_id=request.cookies.get('ssnid')
					if session_id:
						session=SessionManager(session_id,driver=Config.session.driver_name,config=Config.session.all)
					else:
						session=SessionManager(driver=Config.session.driver_name,config=Config.session.all)
					user_id=session[Config.authentication.auth_id]
					if not user_id :
						res=aiohttp.web.HTTPFound(Config.authentication.login_url)
						return res
					else:
						unss=request.cookies.get('unss') or request.GET.get('unss')
						if not unss:
							yield from request.post()
							unss=request.POST.get('unss')
							if not unss:
								res=aiohttp.web.HTTPFound(Config.authentication.login_url)
								return res 
						if session['auth_unss']!=unss:
							res= aiohttp.web.HTTPFound(Config.authentication.login_url)
							return res
			return (yield from handler(request))
			
		return _auth
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
	pass


