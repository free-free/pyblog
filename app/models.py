#!/usr/bin/env python3.5


from   tools.column  import Column
from   tools.field   import String,Int,Float,Text,Boolean
from   tools.model   import Model
from   tools.database    import *
from   tools.log         import *
import time
class User(Model):
	__table__='users'
	id=Column(Int(4,unsigned=True),primary_key=True,null=False,auto_increment=True)
	user_name=Column(String(50),unique_key=True,null=False)
	password=Column(String(100),null=False)
	email=Column(String(50),unique_key=True,null=False)
	user_image=Column(String(300))
	last_login=Column(String(20))
	create_at=Column(Float(),default=time.time())
	gender=Column(Int(1,unsigned=True))
	location=Column(String(50))
	desc=Column(String(600))
class Article(Model):
	__table__='articles'
	id=Column(Int(4,unsigned=True),primary_key=True,null=False,auto_increment=True)
	uid=Column(Int(4,unsigned=True),null=False)
	cate_id=Column(Int(4,unsigned=True),null=False)
	content=Column(Text())
	post_at=Column(Float(),default=time.time())
	modify_at=Column(String(20))
	auth_password=Column(String(100),default="")
	abstract=Column(String(400))
	view_num=Column(Int(4,unsigned=True),default=0)
class Category(Model):
	__table__='categorys'
	id=Column(Int(4,unsigned=True),primary_key=True,auto_increment=True)
	uid=Column(Int(4,unsigned=True))
	cate_text=Column(String(100))
	cate_image=Column(String(200))
	creat_at=Column(Flot(),default=time.time())
	article_num=Column(Int(4,unsigned=True),default=0)
	cate_desc=Column(String(400),default='')
class Comment(Model):
	__table__='comments'
	id=Column(Int(4,unsigned=True),primary_key=True,auto_increment=True)
	uid=Column(Int(4,unsigned=True),null=False)
	article_id=Column(Int(4,unsigned=True))
	comment_text=Column(String(1000))
class Image(Model):
	__table__='images'
	id=Column(Int(4,unsigned=True),primary_key=True,auto_increment=True)
	uid=Column(Int(4,unsigned=True))
	type_id=Column(Int(2,unsigned=True))	
	belong_id=Column(Int(4,unsigned=True))
	url=Column(String(300))
class Music(Model):
	__table__='musics'
	id=Column(Int(4,unsigned=True),primary_key=True,auto_increment=True)
	uid=Column(Int(4,unsigned=True))
	type_id=Column(Int(4,unsigned=True))
	belong_id=Column(Int(4,unsigned=True))
	url=Column(String(300))
#class Need(Model):
#	__table__='needs'
#	id=Column(Int(4,unsigned=True),primary_key=True,null=False,auto_increment=True)
#	user_id=Column(Int(4,unsigned=True),null=False)
#	content=Column(Text(),null=False)
#	create_at=Column(Float(),default=time.time())
#	is_solved=Column(Boolean(),default=False)
#	solved_user_id=Column(Int(4,unsigned=True),default=0)

if __name__=='__main__':
	print(Need().__table__)	
	print(Need().__columns__)
	print(User().__columns__)
	print(User().__table__)
	
