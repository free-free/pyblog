#!/usr/bin/env python3



from field import *
class Column(object):
	__constraints=set([
	'unique_key',
	'primary_key',
	'null',
	'default',
	])
	def __init__(self,c_type,**kw):
		self.constraints=dict()
		self.columnType=''
		if isinstance(c_type,Field):
			self.columnType=c_type.column_type
			for k,v in kw.items():
				if k in self.__constraints:
					self.constraints[k]=v
		else:
			raise TypeError
	def __str__(self):
		info=self.columnType.strip()+':\r\n\t';
		for k,v in self.constraints.items():
			info=info+k+':'+str(v)+'\r\n\t'
		return info
	__repr__=__str__
if __name__=='__main__':
	s=Column(String(20),primary_key=True,default="hello")
	print(s)
			
