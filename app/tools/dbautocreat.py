#-*- coding:utf-8 -*-
import asyncio
import aiomysql
from tools.config import Config


class AutoCreate(obj):
	def __init__(self):
		pass
	def _create_db(self):
		pass
	def _create_field_type(self):
		pass
	def _create_field_primary_key(self):
		pass
	def _create_field_unique_key(self):
		pass
	def _create_auto_increment(self):
		pass
	def _create_default(self):
		pass
	def _create_table(self):
		pass
	def run(self):
		pass

@asyncio.coroutine
def auto_create():
	conn=yield from aiomysql.connect(db=Config.database.database,
					host=Config.database.host,
					password=Config.database.password,
					user=Config.database.user)
	cursor =yield from conn.cursor()
	yield from cursor.execute('show databases;')
	ret=yield from cursor.fetchall()
	print(ret)

if __name__=='__main__':
	loop=asyncio.get_event_loop()
	loop.run_until_complete(asyncio.wait([auto_create()]))
	loop.close()

	


