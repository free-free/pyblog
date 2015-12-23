#!/usr/bin/env python3

class Field(object):
	def __init__(self,c_type):
		self.column_type=c_type
	def __str__(self):
		return '<%s,%s>'%(self.__class__.__name__,self.column_type)

class String(Field):
	def __init__(self,type_length):
		if int(type_length)<=255:
			super().__init__(' char(%s) '%type_length)
		elif 65535>=int(type_length)>=255:
			super().__init__(' varchar(%s) '%type_length)
		else:
			super().__init__('text') 
		

class Int(Field):

	def __init__(self,type_length):
			if type_length<=1:
				super().__init__('tinyint')
			elif type_length<=2:
				super().__init__('smallint')
			elif type_length<=4:
				super().__init__('int')
			else:
				super().__init__('bigint')


if __name__=='__main__':
	s=String(25)
	i=Int(2)
	print(i)
	print(s)
