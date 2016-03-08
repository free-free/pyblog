#!/usr/bin/env python3.5
import os,time,asyncio,json
from   datetime import datetime
from   aiohttp import web
import logging;logging.basicConfig(level=logging.INFO)
from   tools.log import Log
from   tools.httptools import Middleware,Route 

@Route.get('/')
def index():
	return '<h1>Hello</h1>'
@Route.get('/user/{id}/{comment}')
def user(id,comment):
	return '<h1>%s,%s</h1>'%(id,comment)

@asyncio.coroutine
def init(loop):
	print(Middleware.allmiddlewares())
	app=web.Application(loop=loop,middlewares=Middleware.allmiddlewares())

	Route.register_route(app)
	print(Route._routes)
	srv=yield from  loop.create_server(app.make_handler(),'127.0.0.1',8000)
	logging.info('server started at http://127.0.0.1:8000')
	Log.info("server startd at http://127.0.0.1:8000")
	return srv

if __name__=="__main__":
	loop=asyncio.get_event_loop()
	loop.run_until_complete(init(loop))
	loop.run_forever()


