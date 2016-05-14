#!/usr/bin/env python3.5

import os

from	pyblog.orm.field import *
class Column(object):
	def __init__(self,c_type,**kw):
		self.columnType=""
		self.constraints={'unique_key':False,'primary_key':False,'null':True,'default':'','auto_increment':False}
		if isinstance(c_type,Field):
			self.columnType=c_type.column_type
			for k,v in kw.items():
				if k in self.constraints:
					self.constraints[k]=v
		else:
			raise TypeError('%s not supported type'%c_type)
	def __str__(self):
		info=self.columnType.strip()+':\r\n\t';
		for k,v in self.constraints.items():
			info=info+k+':'+str(v)+'\r\n\t'
		return info
	__repr__=__str__




if __name__=='__main__':
	s=Column(String(20),primary_key=True,default="hello")
	print(s)
		
