#!/usr/bin/env python3.5
from tools.application import Application
from tools.template import Template
from tools.httptools import Route
from models import *
import hashlib
import uuid
@Route.get('/')
def index(app):
	user=yield from  User().findone()
	print(user.email)
	app.set_cookie('sl',uuid.uuid1())
	app.set_cookie('date',uuid.uuid4())
	#app.clear_cookie('sl')
	return Template('index.html').render(user=user)
@Route.get('/clc_cookie')
def clc_cookie(app):
	app.clear_all_cookies()
	return 'ok'
@Route.get('/get_cookie')
def get_cookie(app):
	sl=app.get_cookie('sl')
	date=app.get_cookie('date')
	print(app.get_all_cookies())
	return '%s\r\n%s'%(sl,date)
@Route.get('/user/{id}/comment/{comment}')
def user(app,id,comment):
	u=User()
	user=yield from u.findone()
	return Template('index.html').render(user=user)
@Route.get('/user/register')
def get_register(app):
	return Template("register.html").render()
@Route.post('/user/register')
def register(app):
	u=User()
	u.user_name=app.get_argument('username')
	md5=hashlib.md5()
	password=app.get_argument('password')
	md5.update(password.encode('utf-8'))
	u.password=md5.hexdigest()
	u.email=app.get_argument('email')
	yield from u.save()
	return '<h1>OK</h1>'
if __name__=="__main__":
	app=Application()
	app.run()

