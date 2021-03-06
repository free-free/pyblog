#!/usr/bin/env python3.5

from   pyblog.orm.column  import Column
from   pyblog.orm.field   import String,Int,Float,Text,Boolean
from   pyblog.orm.model   import Model
import time
class User(Model):
	__table__='users'
	id=Column(Int(4,unsigned=True),primary_key=True,null=False,auto_increment=True)
	user_name=Column(String(50),unique_key=True,null=False)
	password=Column(String(100),null=False)
	email=Column(String(50),unique_key=True,null=False)
	user_image=Column(String(300))
	last_login=Column(String(30))
	create_at=Column(String(30))
	gender=Column(Int(1,unsigned=True))
	location=Column(String(50))
	description=Column(String(600))
class Article(Model):
	__table__='articles'
	id=Column(Int(4,unsigned=True),primary_key=True,null=False,auto_increment=True)
	uid=Column(Int(4,unsigned=True),null=False)
	category_id=Column(Int(4,unsigned=True),null=False)
	title=Column(String(200))
	content=Column(Text())
	post_at=Column(String(30))
	modify_at=Column(String(30))
	auth_password=Column(String(100),default="")
	description=Column(String(400))
	view_num=Column(Int(4,unsigned=True),default=0)
class Category(Model):
	__table__='categorys'
	id=Column(Int(4,unsigned=True),primary_key=True,auto_increment=True)
	uid=Column(Int(4,unsigned=True))
	text=Column(String(100))
	image_url=Column(String(200))
	create_at=Column(String(30))
	article_num=Column(Int(4,unsigned=True),default=0)
	description=Column(String(400),default='')
class Comment(Model):
	__table__='comments'
	id=Column(Int(4,unsigned=True),primary_key=True,auto_increment=True)
	uid=Column(Int(4,unsigned=True),null=False)
	type_id=Column(Int(4,unsigned=True))
	belong_id=Column(Int(4,unsigned=True))
	comment_at=Column(String(30))
	article_id=Column(Int(4,unsigned=True))
	comment_text=Column(String(1000))
class Image(Model):
	__table__='images'
	id=Column(Int(4,unsigned=True),primary_key=True,auto_increment=True)
	uid=Column(Int(4,unsigned=True))
	type_id=Column(Int(1,unsigned=True))	
	belong_id=Column(Int(4,unsigned=True))
	upload_at=Column(String(30))
	image_url=Column(String(300))
class Music(Model):
	__table__='musics'
	id=Column(Int(4,unsigned=True),primary_key=True,auto_increment=True)
	uid=Column(Int(4,unsigned=True))
	upload_at=Column(String(30))
	type_id=Column(Int(1,unsigned=True))
	belong_id=Column(Int(4,unsigned=True))
	music_name=Column(String(30))
	music_url=Column(String(300))
class Share(Model):
	__table__='shares'
	id=Column(Int(4,unsigned=True),primary_key=True,auto_increment=True)
	uid=Column(Int(4,unsigned=True))
	type_id=Column(Int(1,unsigned=True))
	share_at=Column(String(30))
	share_url=Column(String(300))
	title=Column(String(100))
	description=Column(String(100))
class Book(Model):
	__table__='books'
	id=Column(Int(4,unsigned=True),primary_key=True,auto_increment=True)
	name=Column(String(100))
	author=Column(String(100))
	state=Column(Int(1,unsigned=True))
	description=Column(String(500))
	comment=Column(String(1000))
#class Need(Model):
#	__table__='needs'
#	id=Column(Int(4,unsigned=True),primary_key=True,null=False,auto_increment=True)
#	user_id=Column(Int(4,unsigned=True),null=False)
#	content=Column(Text(),null=False)
#	create_at=Column(Float(),default=time.time())
#	is_solved=Column(Boolean(),default=False)
#	solved_user_id=Column(Int(4,unsigned=True),default=0)

if __name__=='__main__':
	#print(Need().__table__)	
	#print(Need().__columns__)
	#print(User().__columns__)
	#print(User().__table__)
	print(User().__table__)
	print(User().__columns__)
	

