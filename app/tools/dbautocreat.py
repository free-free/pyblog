#-*- coding:utf-8 -*-
import asyncio
import aiomysql
from tools.config import Config


class AutoCreate(object):
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
class MysqlAutoCreate(AutoCreate):
	def __init__(self,model,config):
		self._config=config
		self._table=model.__table__
		self._fields=model.__columns__
	@asyncio.coroutine
	def _create_connection(self):
		type(self)._conn=yield from aiomysql.connect(db=self._config['database'],
								user=self._config['user'],
								host=self._config['host'],
								password=self._config['password'])						
	@asyncio.coroutine
	def _db_is_exists(self):
		cursor=yield from self._conn.cursor()
		yield from cursor.execute('use '+self._config['database'])
		ret=yield from cursor.fecthall()
	def _create_db(self,model):
		pass	
@asyncio.coroutine
def auto_create():
	conn=yield from aiomysql.connect(db=Config.database.database,
					host=Config.database.host,
					password=Config.database.password,
					user=Config.database.user)
	cursor =yield from conn.cursor()
	yield from cursor.execute('use xx;')
	ret=yield from cursor.fetchall()
	print(ret)

if __name__=='__main__':
	loop=asyncio.get_event_loop()
	loop.run_until_complete(asyncio.wait([auto_create()]))
	loop.close()

	


