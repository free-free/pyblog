#!/usr/bin/env python3
import asyncio
import logging;logging.basicConfig(level=logging.ERROR)
try:
	import aiomysql
except Exception:
	logging.error('aiomysql module not Found')
	exit()


@asyncio.coroutine
def create_pool(loop,**kw):
	global __pool
	__pool=yield from aiomysql.create_pool(
		host=kw.get('host','localhost'),
		port=kw.get('port',3306),
		user=kw['user'],
		password=kw['password'],
		db=kw['db'],
		charset=kw.get('charset','utf-8'),
		autocommit=kw.get('autocommit',True),
		maxsize=kw.get('maxsize',10),
		minsize=kw.get('minsize',1),
		loop=loop
	)
@asyncio.coroutine
def select(sql,args,size=None):
	log(sql,args)
	global __pool
	with (yield from __pool) as connection:
		cursor=yield from connection.cursor(aiomysql.DictCursor)
		yield from cursor.execute(sql.replace('?','%s'),args or ())
		if size:
			records=yield from cursor.fetchmany(size)
		else:
			recors=yield from cursor.fetchall()
		yield from cursor.close()
		return records
@asyncio.coroutine
def execute(sql,args):
	global __pool
	with (yield from __pool) as connections:
		try:
			cursor=yield from connection.cursor(aiomysql.DictCursor)
			yield from cursor.excute(sql.replace('?','%s'),args or ())
			affectedrow=cursor.rowcount
			yield from cursor.close()
		except BaseException as e:
			raise e
		return affectedrow

		
		
			
