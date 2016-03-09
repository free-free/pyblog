# -*- coding:utf-8 -*-
import os,time,asyncio,json
import logging
logging.basicConfig(level=logging.ERROR)
try:
	from aiohttp import web
except ImportError:
	logging.error("Can't import module aiohttp")
from tools.log import Log
from tools.httptools import Middleware,Route
from tools.template  import Template
from tools.config import Config
from tools.database import create_pool
logging.basicConfig(level=logging.INFO)
class Application(web.Application):
	def __init__(self,loop):
		self._loop=loop
		super(Application,self).__init__(loop=loop,middlewares=Middleware.allmiddlewares())
	@asyncio.coroutine
	def run(self,addr='127.0.0.1',port='8000'):
		Template.init(self)
		Route.register_route(self)
		pool=yield from create_pool(self._loop)
		srv=yield from self._loop.create_server(self.make_handler(),addr,port)
		logging.info("server start at http://%s:%s"%(addr,port))
		print("server start at http://%s:%s"%(addr,port))
		return srv
	
