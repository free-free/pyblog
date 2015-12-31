#!/usr/bin/env python3
import os
os.sys.path.append(os.path.join(os.path.dirname(__file__),'../'))
import asyncio
import logging;logging.basicConfig(level=logging.ERROR)
from   tools.log import *
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
				user=kw.get('user','root'),
				password=kw['password'],
				db=kw['db'],
				loop=loop
	)

@asyncio.coroutine
def select(sql,size=None):
	Log.info(sql)
	global __pool
	with (yield from __pool) as conn:
		cursor=yield from conn.cursor(aiomysql.DictCursor)
		yield from cursor.execute(sql)
		if size:
			records=yield from cursor.fetchmany(size)
		else:
			records=yield from cursor.fetchall()
		yield from cursor.close()
		return records

@asyncio.coroutine
def execute(sql,autocommit=True):
	Log.info(sql)
	with (yield from __pool) as conn:
		if not autocommit:
			conn.begin()
		try:
			cursor=yield from conn.cursor()
			yield from cursor.execute(sql)
			affectedrow=cursor.rowcount
			yield from cursor.close()
			if not autocommit:
				conn.commit()
		except BaseException as e:
			if not autocommit:
				conn.rollback()
			raise e
		return affectedrow			
if __name__=='__main__':
	loop = asyncio.get_event_loop()
	create_pool(loop,db='pyblog',password='526114')
	#loop.run_until_complete(asyncio.wait(tasks))
	
