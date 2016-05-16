#-*- coding:utf-8 -*-
from  database_abstract import AbstractDatabaseDriver
import aiomysql
import asyncio

class MysqlDriver(AbstractDatabaseDriver):
	def __init__(self,
			host,
			port,
			user,
			password,
			db,
			loop=None,
			pool=None):

		assert isinstance(host,str)
		assert isinstance(port,(int,str))
		assert isinstance(user,str)
		assert isinstance(password,str)
		assert isinstance(db,(str,type(None)))
		self.__host=host
		self.__port=int(port)
		self.__user=user
		self.__password=password
		self.__db=db
		self.__loop=loop
		self.__pool=pool
		self.__connection_yield=False
		if not self.__pool:
			self.__connection=aiomysql.connect(
							host=self.__host,
							port=self.__port,
							user=self.__user,
							password=self.__password,
							db=self.__db,
							loop=self.__loop
							)
		else:
			self.__connection=None
	@asyncio.coroutine
	def connection(self):
		if not self.__connection_yield:
			if self.__connection:
				self.__connection=yield from self.__connection
			else:
				self.__connection=yield from self.__pool
			self.__connection_yield=True
	@asyncio.coroutine
	def query(self,sql):
		yield from self.connection()
		cursor=yield from self.__connection.cursor()
		yield from cursor.execute(sql)
		ret=yield from cursor.fetchall()
		return ret
	@asyncio.coroutine
	def insert(self,sql):
		yield from self.connection()
		cursor=yield from self.__connection.cursor()
		yield from cursor.execute(sql)
		yield from self.__connection.commit()
	@asyncio.coroutine
	def update(self,sql):
		yield from self.connection()
		cursor=yield from self.__connection.cursor()
		yield from cursor.execute(sql)
		yield from self.__connection.commit()
		
	@asyncio.coroutine
	def delete(self,sql):
		yield from self.connection()
		cursor=yield from self.__connection.cursor()
		yield from cursor.execute(sql)
		yield from self.__connection.commit()
	@asyncio.coroutine
	def select_db(self,db):
		yield from self.connection()
		yield from self.__connection.select_db(db)
	@asyncio.coroutine
	def close(self):
		yield from self.connection()
		self.__connection.close()
	
			
if __name__=='__main__':
	pass
	r'''
	@asyncio.coroutine
	def go(loop):
		m=MysqlDriver('127.0.0.1','3306','root','526114','pyblog')
		yield from m.delete("delete from users where id=6")
	loop=asyncio.get_event_loop()
	loop.run_until_complete(go(loop))
						
	'''


