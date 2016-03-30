#-*- coding:utf-8 -*-
from tools.application import Application
from tools.httptools import Route
from models import *

@Route.get('/')
def index_handler(app):
	app.render("index.html")

@Route.get('/articles')
def article_list_handler(app):
	app.render("article.html")
@Route.get('/history')
def article_history_handler(app):
	app.render("list.html")
@Route.get('/about')
def aboutme_handler(app):
	app.render("me.html")



if __name__=='__main__':
	app=Application()
	app.run()
