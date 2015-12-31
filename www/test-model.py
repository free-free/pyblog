#!/usr/bin/env python3

from tools.database import *
from models import *
import asyncio
import sys

def test(loop):
	yield from create_pool(loop,db='pyblog',password='526114')
	u=User(user_name='koude',email='18281573692@163.com',password='526114')
	yield from u.save()

	
if __name__=='__main__':
	loop=asyncio.get_event_loop()
	loop.run_until_complete(asyncio.wait([test(loop)]))
	loop.close()
	if loop.is_closed():
		sys.exit(0)

	

