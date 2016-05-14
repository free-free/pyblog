#-*- coding:utf-8 -*-
from tools.application import Application
from tools.httptools import Route
from models import *
from music_handler import *
from user_handler import *
from article_handler import *
import aiohttp
@Route.get('/')
def index_handler(app):
	app.render("index.html")
if __name__=='__main__':
	app=Application()
	app.run()
