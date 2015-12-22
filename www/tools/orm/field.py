#!/usr/bin/env python3

class Field(object):
	def __init__(self,name,c_type,**kw):
		self.name=name
		self.column_type=c_type
		self.primary_key=kw.get('primary_key') if 'primary_key' in kw else False
		self.unique_key=kw.get('unique_key') if 'unique_key' in kw else False
		self.default=kw.get('default') if 'default' in kw else ''
		self.Null=kw.get('null')  if 'null'in kw else False
	def __str__(self):
		return '<%s,%s:%s>'%(self.__class__.__name__,self.name,self.column_type)

class StringField(Field):
	def __init__(self,name,*,char=False,length=255,**kw):
		if char:
			super().__init__(name,' char(%s) '%length,**kw)
		else:
			super().__init__(name,' varchar(%s) '%length,**kw)

class IntField(Field):
	__type=dict({1:'tinyint',2:'smallint',4:'int',8:'bigint'})
	def __init__(self,name,*,uint=True,length=4,**kw):
		if uint:
			super().__init__(name,'%s unsigned '%self.__type.get(length),**kw)
		else:
			super().__init__(name,' %s '%self.__type.get(length),**kw)



if __name__=='__main__':
	s=StringField('name',char=False,length=382)
	print(s)
