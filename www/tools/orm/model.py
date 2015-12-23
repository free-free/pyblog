#!/usr/bin/env python3


from field import *
class ModelMetaclass(type):
	def __new__(cls,name,bases,attrs):
		if name=='Model':
			return type.__new__(cls,name,bases,attrs):
		columnsDict=dict()
		tableName=attrs.get('__table__') or name
                primaryKey='None'		
		for c_name,v in attrs.items():
			if isinstance(v,Field):
				columnsDict[c_name]=v		
				if v.primary_key:
					if primaryKey:
						raise RuntimeError('Duplicate primary key find in %s'%k)
					primaryKey=c_name
				
		for column in columnsDict.keys():
			attrs.pop(column)
		escaped_fields=list(map(lambda f:'`%s`'%f,colunmsDict.keys()))
		attrs['__columns__']=columnsDict
		attrs['__table__']=tableName
		attrs['__primary_key__']=primaryKey
		return type.__new__(cls,name,bases,attrs)

class Model(dict,metaclass=ModelMetaclass):
	
		
		
				

			
		

