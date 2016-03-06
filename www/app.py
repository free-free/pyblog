#!/usr/bin/env python3.5
import os,time,asyncio,json
from   datetime import datetime
from   aiohttp import web
import logging;logging.basicConfig(level=logging.INFO)
from   tools.log import Log

def index(request):
	return web.Response(body=b'<h1>God</h1>')


@asyncio.coroutine
def init(loop):
	app=web.Application(loop=loop)
	app.router.add_route('GET','/',index)
	srv=yield from  loop.create_server(app.make_handler(),'127.0.0.1',8000)
	logging.info('server started at http://121.42.169.254:80')
	Log.info("server startd at http://127.0.0.1:8000")
	return srv

if __name__=="__main__":
	loop=asyncio.get_event_loop()
	loop.run_until_complete(init(loop))
	loop.run_forever()

