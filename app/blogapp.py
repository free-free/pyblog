#-*- coding:utf-8 -*-
from tools.application import Application
from tools.httptools import Route
from models import *

@Route.get('/')
def index_handler(app):
	return app.render("index.html")

