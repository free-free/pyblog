#!/usr/bin/env python3


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
	image=Column(String(300))
	create_at=Column(Float(),default=time.time())

class Need(Model):
	__table__='needs'
	id=Column(Int(4,unsigned=True),primary_key=True,null=False,auto_increment=True)
	user_id=Column(Int(4,unsigned=True),null=False)
	content=Column(Text(),null=False)
	create_at=Column(Float(),default=time.time())
	is_solved=Column(Boolean(),default=False)
	solved_user_id=Column(Int(4,unsigned=True),default=0)

if __name__=='__main__':
	print(Need().__table__)	
	print(Need().__columns__)
	print(User().__columns__)
	print(User().__table__)
	
