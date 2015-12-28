#!/usr/bin/env python3

from datetime import datetime
import os
class Log(object):
	_logPath=os.path.abspath(os.path.join(os.path.dirname(__file__),'../../log'))
	_logName='pyblog'+str(datetime.date(datetime.now()))+'.log'
	_logFormat=""" [%s]  level:%s ==> %s \r\n"""
	def __init__(self):
		pass
	@classmethod
	def info(cls,info):
		with open(os.path.join(cls._logPath,cls._logName),'a+') as f:
			f.write(cls._logFormat%(datetime.now(),'INFO',info))
	@classmethod
	def warning(cls,info):
		with open(os.path.join(cls._logPath,cls._logName),'a+') as f:
			f.write(cls._logFormat%(datetime.now(),'WARNING',info))
	@classmethod
	def error(cls,info):
		with open(os.path.join(cls._logPath,cls._logName),'a+') as f:
			f.write(cls._logFormat%(datetime.now(),'ERROR',info))
	@classmethod
	def getLogPath(cls):
		return os.path.join(cls._logPath,cls._logName)
	@classmethod
	def setLogPath(cls,path):
		cls._logPath=path
	
if __name__=='__main__':
	sql='select * from user'.upper()
	Log.error(sql)
	Log.warning(sql)
	Log.info(sql)


		
