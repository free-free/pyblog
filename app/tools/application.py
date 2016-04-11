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
from tools.database import DB
from tools.session import SessionManager
logging.basicConfig(level=logging.INFO)
class Application(web.Application):
	def __init__(self):
		self._loop=asyncio.get_event_loop()
		super(Application,self).__init__(loop=self._loop,middlewares=Middleware.allmiddlewares())
	def run(self,addr='127.0.0.1',port='8000'):
		self._server=self._loop.run_until_complete(self.get_server(addr,port))
		try:
			self._loop.run_forever()
		except KeyboardInterrupt:
			pass
		finally:
			self._db_pool.close()
			self._loop.run_until_complete(self._db_pool.wait_closed())
			self._server.close()
			self._loop.run_until_complete(self._server.wait_closed())
			self._loop.run_until_complete(self.shutdown())
			self._loop.run_until_complete(self._handler.finish_connections(60))
			self._loop.run_until_complete(self.cleanup())
		self._loop.close()
	@asyncio.coroutine
	def get_server(self,addr,port):	
		Template.init(self)
		Route.register_route(self)
		self._db_pool=yield from DB.createpool(self._loop)
		#pool=yield from create_pool(self._loop)
		self._handler=self.make_handler()
		server=yield from self._loop.create_server(self._handler,addr,port)
		logging.info("server start at http://%s:%s"%(addr,port))
		Log.info("server start at http://%s:%s"%(addr,port))
		print("server start at http://%s:%s"%(addr,port))
		return server
