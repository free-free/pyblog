#-*- coding:utf-8 -*-
import logging
logging.basicConfig(level=logging.ERROR)


class FileSystemAdataper(object):
	def __init__(self,*args,**kw):
		pass
	def move(self,src,dest):
		pass
	def copy(self,src,dest):
		pass
	def delete(self,src):
		pass
	def mkdir(self,dir_name):
		pass
	def rmdir(self,dir_name):
		pass
