#!/usr/bin/env python3
import asyncio
import aiomysql
loop = asyncio.get_event_loop()

@asyncio.coroutine
def go():
	global pool
	pool = yield from aiomysql.create_pool(host='127.0.0.1', port=3306,user='root', password='526114',db='pyblog', loop=loop)
	with (yield from pool) as conn:
		cur=yield from conn.cursor()
		yield from cur.execute("SELECT * from user")
		r=yield from cur.fetchall()	
		print(r)
	pool.close()
	yield from pool.wait_closed()

loop.run_until_complete(go())
if __name__=='__main__':
	print(__file__)
