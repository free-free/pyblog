#-*- coding:utf-8 -*-
from tools.httptools import Route
from models import User

@Route.get('/{username}')
def get_user_handler(app,username):
	print(username)
	app.render("admin.html")

