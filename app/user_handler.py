#-*- coding:utf-8 -*-
from tools.httptools import Route
from tools.helper import locale_translate
from models import User
import time
import hashlib

@Route.get('/{username}')
def get_user_index_page_handler(app,username):
	m=User()
	data=yield from m.where('user_name','=',username).findone()
	if len(data)==0:
		app.set_status(404)
	else:
		app.render("index.html")

@Route.get('/login')
def get_login_handler(app):
	app.render("signin.html")

@Route.post('/login')
def post_login_handler(app):
	m=User()
	email=app.get_argument("email","").strip()
	password=app.get_argument("password","").strip()
	data=yield from m.where('email','=',email).fields(['id','user_name','password','email','last_login']).findone()
	if len(data)==0:
		app.render("signin.html",email_error=locale_translate("message:login.email"),email=email,password=password)
		return ''
	sha1=hashlib.sha1()
	sha1.update(password.encode('utf-8'))
	password=sha1.hexdigest()
	if data['password']!=password:
		app.render("signin.html",password_error=locale_translate("message:login.password"),email=email,password="")
		return ''
	app.session['id']=data['id']
	app.session['user_name']=data['user_name']
	app.session['password']=data['password']
	app.session['email']=data['email']
	app.session['last_login']=data['last_login']
	app.session_end()
	is_ok=yield from m.where('id','=',data['id']).update({'last_login':int(time.time())})
	app.redirect('/%s/home'%data['user_name'])

@Route.get('/logout',auth=True)
def get_logout_handler(app):
	user_name=app.session['user_name']
	app.session_destroy()
	app.redirect('/%s'%user_name)

@Route.get('/register')
def get_register_handler(app):
	app.render("register.html")

@Route.post('/register')
def post_register_handler(app):
	m=User()
	username=app.get_argument("user_name","").strip()
	email=app.get_argument("email","").strip() 
	password=app.get_argument('password','').strip()
	data=yield from m.where("email",'=',email).findone()
	if len(data)>=1:
		app.render("register.html",email_error=locale_translate("message:register.email"),user_name=username,email=email,password=password)
		return ''
	data=yield from m.where("user_name",'=',username).findone()
	if len(data)>=1:
		app.render("register.html",user_name_error=locale_translate("message:register.username"),user_name=username,email=email,password=password)
		return ''
	m.user_name=username
	m.email=email
	sha1=hashlib.sha1()
	sha1.update(password.encode('utf-8'))
	m.password=sha1.hexdigest()
	m.create_at=str(int(time.time()))
	m.last_login=str(int(time.time()))
	is_ok=yield from m.save()
	if is_ok:
		app.session['user_name']=username
		app.session['password']=password
		app.session['email']=email
		app.session['last_login']=m.last_login
		app.session_end()
		app.redirect("/%s/home"%username)
	else:
		app.render("register.html")

@Route.get("/{username}/profile")
def get_user_profile_handler(app,username):
	m=User()
	data=yield from m.where('user_name','=',username).findone()
	if len(data)==0:
		return {'404':"page not found"}
	else:
		app.render("me.html")
	app.render("me.html")

@Route.get('/{username}/activity')
def get_user_activity_handler(app,username):
	m=User()
	data=yield from m.where('user_name','=',username).findone()
	if len(data)==0:
		return {'404':'page not found'}
	else:
		app.render('list.html')

@Route.get('/{username}/home',auth=True)
def get_user_home_page_handler(app,username):
	if username==app.session['user_name']:
		app.render('admin.html')
	else:
		app.redirect('/login')
