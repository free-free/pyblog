#-*- coding:utf-8 -*-
from tools.httptools import Route
from models import User

@Route.get('/{username}')
def get_user_handler(app,username):
	print(username)
	app.render("admin.html")

@Route.get('/login')
def get_login_handler(app):
	app.render("signin.html")
@Route.post('/login')
def post_login_handler(app):
	print(app.get_argument("email"))
	print(app.get_argument("password"))
	app.redirect('/whoami')

@Route.get('/register')
def get_register_handler(app):
	app.render("register.html")
@Route.post('/register')
def post_register_handler(app):
	print(app.get_argument("email"))
	print(app.get_argument("password"))
	print(app.get_argument("user_name"))
	app.redirect("/whoami")


@Route.get("/{username}/profile")
def get_user_profile_handler(app,username):
	print(username)
	app.render("me.html")
@Route.get('/{username}/activity')
def get_user_activity_handler(app,username):
	print(username)
	app.render("list.html")

