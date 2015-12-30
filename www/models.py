#!/usr/bin/env python3
from tools.orm.column   import Column
from tools.orm.field   import String,Int,Float,Text,Boolean
from tools.orm.model   import Model
from tools.database import *
from tools.log     import *
import time
class User(Model):
	__table__='users'
	id=Column(Int(4,unsigned=True),primary_key=True,null=False)
	user_name=Column(String(50),unique_key=True,null=False)
	password=Column(String(100),unique_key=True,null=False)
	email=Column(String(50),unique_key=True,null=False)
	image=Column(String(500))
	creat_at=Column(Float(),default=time.time)

class Need(Model):
	__table__='needs'
	id=Column(Int(4,unsigned=True),primary_key=True,null=False)
	user_id=Column(Int(4,unsigned=True),null=False)
	content=Column(Text(),null=False)
	create_at=Column(Float(),default=time.time)
	is_sovled=Column(Boolean(),default=False)
	sovled_user_id=Column(Int(4,unsigned=True),null=False)

if __name__=='__main__':
	
	print(Need().__columns__)
	print(User().__columns__)
	
