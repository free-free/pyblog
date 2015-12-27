#!/usr/bin/env python3

from field import *
from column import *
class ModelMetaclass(type):
	def __new__(cls,name,bases,attrs):
		if name=='Model':
			type.__new__(cls,name,bases,attrs)
		tableName=attrs.get('__table__') or name
		primaryKey=None
		tableColumns=dict()
		for c_name,c_type in attrs.items():
			if isinstance(c_type,Column):
				tableColumns[c_name]=dict({
				'type':c_type.columnType,
				'constraints':c_type.constraints
				})
				if 'primary_key' in c_type.constraints:
					if primaryKey:
						raise RuntimeError('Duplicate primary key find in %s'%k)
					primaryKey=c_name
		for column in tableColumns.keys():
			attrs.pop(column)
		escaped_fields=list(map(lambda f:'`%s`'%f,tableColumns.keys()))
		attrs['__columns__']=tableColumns
		attrs['__table__']=tableName
		attrs['__primary_key__']=primaryKey
		return type.__new__(cls,name,bases,attrs)

class Model(dict,metaclass=ModelMetaclass):
	def __init__(self,**kw):
		columns=dict()
		for k in self.__columns__:
			columns[k]=self.__columns__[k]['constraints']['default']
		for  k,v in kw.items():
			if k not in self.__columns__.keys():
				raise AttributeError(r'%s has no attribute %s'%(self.__class__.__name__,key))
			else:
				columns[k]=v
		super(Model,self).__init__(self,**columns)
	def __setattr__(self,key,value):
		self[key]=value
	def __getattr__(self,key):
		try:
			return self[key]
		except KeyError:
			raise AttributeError(r"'%s' has no attribute %s "%(self.__class__.__name__,key))
	def get(self):
		print(self.__columns__)
		print(self.__table__)


class User(Model):
	name=Column(String(20),primary_key=True,unique_key=True,default='')
	age=Column(Int(1),default='')
	email=Column(String(20),unique_key=True)

if __name__=='__main__':
	m=User()
	print(m.name)
