#!/usr/bin/env python3

from tools.database import *
from models import *
import asyncio
if __name__=='__main__':
	loop=asyncio.get_event_loop()
	create_pool(db='pyblog',password='526114',loop=loop)
	

