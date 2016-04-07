#-*- coding:utf-8 -*-
from tools.application import Application
from tools.httptools import Route
from models import *
from music_handler import *
from user_handler import *
@Route.get('/')
def index_handler(app):
	app.render("index.html")
@Route.get('/articles')
def get_article_list_handler(app):
	app.render("article.html")
@Route.get('/history')
def get_article_history_handler(app):
	app.render("list.html")
@Route.get('/about')
def get_aboutme_handler(app):
	app.render("me.html")

if __name__=='__main__':
	app=Application()
	app.run()
