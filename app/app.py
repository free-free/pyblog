#!/usr/bin/env python3.5
from tools.application import Application
from tools.template import Template
from tools.httptools import Route
from models import *
@Route.get('/')
def index():
	user=yield from  User().findone()
	print(user.email)
	return Template('index.html').render()
@Route.get('/user/{id}/comment/{comment}')
def user(id,comment):
	return '<h1>%s,%s</h1>'%(id,comment)

if __name__=="__main__":
	loop=asyncio.get_event_loop()
	app=Application(loop)
	loop.run_until_complete(app.run())
	loop.run_forever()

