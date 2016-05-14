#!/usr/bin/env python3.5

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
			pass		
		
class Int(Field):
	def __init__(self,type_length,*,unsigned=False):
			un=''
			if unsigned==True:
				un=' unsigned '	
			if type_length<=1:
				super().__init__('tinyint%s'%un)
			elif type_length<=2:
				super().__init__('smallint%s'%un)
			elif type_length<=4:
				super().__init__('int%s'%un)
			else:
				super().__init__('bigint%s'%un)

class Boolean(Field):
	def __init__(self):
		super().__init__('boolean')
class Float(Field):
	def __init__(self):
		super().__init__('float')
class Text(Field):
	def __init__(self):
		super().__init__('text')


if __name__=='__main__':
	s=String(25)
	s=Int(4,unsigned=True)
	i=Int(2)
	print(i)
	print(s)
