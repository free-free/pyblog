#!/usr/bin/env python3.5
from tools.application import Application
from tools.template import Template
from tools.httptools import Route
from models import *
import hashlib
@Route.get('/')
def index():
	user=yield from  User().findone()
	print(user.email)
	return Template('index.html').render()
@Route.get('/user/{id}/comment/{comment}')
def user(id,comment):
	u=User()
	user=yield from u.findone()
	return Template('index.html').render(user=user)
@Route.get('/user/register')
def get_register():
	return Template("register.html").render()
@Route.post('/user/register')
def register(username,email,password):
	u=User()
	u.user_name=username
	md5=hashlib.md5()
	md5.update(password.encode('utf-8'))
	u.password=md5.hexdigest()
	u.email=email
	yield from u.save()
	return '<h1>OK</h1>'
if __name__=="__main__":
	app=Application()
	app.run()

