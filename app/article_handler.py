#-*- coding:utf-8 -*-
from tools.httptools import Route
from models import Article,User

@Route.get('/{username}/articles/{article_id}.html')
def get_article_handler(app,username,article_id):
	print(username,'==>',article_id)
	app.render('article.html')
	

