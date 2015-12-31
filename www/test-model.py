#!/usr/bin/env python3

from tools.database import *
from models import *
import asyncio
import sys
@asyncio.coroutine
def test_users_table(loop):
	yield from create_pool(loop,db='pyblog',password='526114')
	yield from User(user_name='ab9999999',email='hudehuide@qq.com',password='526114').save()
@asyncio.coroutine
def test_needs_table(loop):
	yield from create_pool(loop,db='pyblog',password='526114')
	n=Need()
	n.user_id=9
	n.content="I need someone take a mathemathic class for me "
	yield from n.save()
	
if __name__=='__main__':
	loop=asyncio.get_event_loop()
	loop.run_until_complete(asyncio.wait([test_needs_table(loop),test_users_table(loop)]))
	loop.close()
	sys.exit(0)

	

