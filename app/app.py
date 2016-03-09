#!/usr/bin/env python3.5
import os,time,asyncio,json
from   datetime import datetime
from   aiohttp import web
import logging;logging.basicConfig(level=logging.INFO)
from   tools.log import Log
from   tools.httptools import Middleware,Route 
from   tools.template  import Template
from   models import *
from   tools.config import Config
@Route.get('/')
def index():
	user=yield from  User.findall()
	print(user)
	return Template('index.html').render()
@Route.get('/user/{id}/comment/{comment}')
def user(id,comment):
	return '<h1>%s,%s</h1>'%(id,comment)

@asyncio.coroutine
def init(loop):
	print(Middleware.allmiddlewares())
	app=web.Application(loop=loop,middlewares=Middleware.allmiddlewares())
	Template.init(app)
	Route.register_route(app)
	pool=yield from create_pool(loop)
	srv=yield from  loop.create_server(app.make_handler(),'127.0.0.1',8000)
	logging.info('server started at http://127.0.0.1:8000')
	Log.info("server startd at http://127.0.0.1:8000")
	return srv

if __name__=="__main__":
	loop=asyncio.get_event_loop()
	loop.run_until_complete(init(loop))
	loop.run_forever()


