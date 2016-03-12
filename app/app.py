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
	r'''
	u.user_name="coder"
	u.email='18281573692@163.com'
	md5=hashlib.md5()
	md5.update(b'huamgbiao526114')
	u.password=md5.hexdigest()
	yield from u.save()
	'''
	yield from u.where('id','=',1).update({'user_name':'hello'})
	return '<h1>%s,%s</h1>'%(id,comment)

@Route.get('/user/register')
def get_register():
	return Template("register.html").render()
@Route.post('/user/register')
def register(username,email,password):
	u=User()
	u.user_name=username
	
	u.password=hashlib.md4().update(password).hexdigest()
	u.email=email
	u.save()
	return '<h1>OK</h1>'
if __name__=="__main__":
	app=Application()
	app.run()

