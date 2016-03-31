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
@Route.post('/music')
def music_handler(app):
	d=dict();
	d['code']=200
	d['msg']='ok'
	d['type']=3
	d['data']=[
	{'music_name':'CountrintStars','music_url':'http://7xs7oc.com1.z0.glb.clouddn.com/music%2FJason%20Chen%20-%20Counting%20Stars.mp3'},
	]
	return d

if __name__=='__main__':
	app=Application()
	app.run()
