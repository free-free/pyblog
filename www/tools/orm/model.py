#!/usr/bin/env python3

import os
os.sys.path.append(os.path.join(os.path.dirname(__file__),'../..'))

from tools.log import *
from tools.orm.field import *
from tools.orm.column import *
from tools.database import *
import aiomysql
class ModelMetaclass(type):
	def __new__(cls,name,bases,attrs):
		if name=='Model':
			type.__new__(cls,name,bases,attrs)
		tableName=attrs.get('__table__') or name
		primaryKey=[]
		notNull=[]
		uniqueKey=[]
		default=dict()
		tableColumns=dict()
		for c_name,c_type in attrs.items():
			if isinstance(c_type,Column):
				tableColumns[c_name]=dict({
				'type':c_type.columnType,
				'constraints':c_type.constraints
				})
				if len(primaryKey)>=2:
					info=r"Duplicate primary key find in %s"%c_name
					Log.error(info)
					raise RuntimeError(info)
				if c_type.constraints['primary_key']==True:
					primaryKey.append(c_name)
				if c_type.constraints['unique_key']==True:
					uniqueKey.append(c_name)
				if c_type.constraints['null']==False:
					notNull.append(c_name)
				if not c_type.constraints['default']==None:
					default[c_name]=c_type.constraints['default']	
		for column in tableColumns.keys():
			attrs.pop(column)
		escaped_fields=list(map(lambda f:'`%s`'%f,tableColumns.keys()))
		attrs['__columns__']=tableColumns
		attrs['__table__']=tableName
		attrs['__primary_key__']=primaryKey[0] if len(primaryKey)>=1 else ''
		attrs['__unique_key__']=uniqueKey
		attrs['__not_null__']=notNull
		attrs['__default__']=default
		attrs['__query__']=dict({'field':False,'where':False,'order':False,'limit':False,'group':False,'having':False})
		return type.__new__(cls,name,bases,attrs)



class Model(dict,metaclass=ModelMetaclass):
	def __init__(self,**kw):
		columns=dict()
		for column_name in self.__columns__:
			columns[column_name]=self.__columns__[column_name]['constraints']['default']
		for  name,value in kw.items():
			if name not in self.__columns__.keys():
				info=r"'%s' has not attribute '%s' "%(self.__class__.__name__,name)
				Log.error(info)
				raise AttributeError(info)
			else:
				columns[name]=value
		super(Model,self).__init__(self,**columns)

	def __setattr__(self,key,value):
		if key in self.__columns__.keys():
			self[key]=value
		else:
			info=r"'%s' has not attribute '%s' "%(self.__class__.__name__,key)
			Log.error(info)
			raise AttributeError(info)

	def __getattr__(self,key):
		if key in self:
			return self[key]	
		else:
			return None
	@asyncio.coroutine
	def findAll(self):
		sql=''
		if self.__query__['field']:
			sql=sql+'select %s '%self.__query__['field']+' from %s '%self.__table__
			self.__query__['field']=False
		else:
			sql=sql+'select * from %s '%self.__table__
		if self.__query__['where']:
			sql=sql+self.__query__['where']
			self.__query__['where']=False
		if self.__query__['order']:
			sql=sql+self.__query__['order']
			self.__query__['order']=False
		if self.__query__['limit']:
			sql=sql+self.__qeury__['limit']
			self.__query__['limit']=False
		if self.__query__['group']:
			sql=sql+self.__query__['group']	
			self.__qeury__['group']=False
		if self.__query__['having']:
			sql=sql+self.__qeury__['having']
			self.__query__['having']=False
		records=yield from select(sql)
		return [self(**k) for k in records]
	@asyncio.coroutine
	def findOne(self):
		re=findAll()
		return re[0]
	@asyncio.coroutine
	def update(self,k,v):
		sql='update `%s` '%self.__table__+' set `%s` = %s '%(k,v)
		if self.__query__['where']:
			sql=sql+self.__query__['where']
			self.__query__['where']=False
		return yield from execute(sql)
	@asyncio.coroutine
	def save(self):
		sql=''
		pass
	@asyncio.coroutine
	def delete(self):
		pass

	def field(self,field):
		if isinstance(field,list):
			self.__query__['field']='('
			field=map(lambda x:'`'+x+'`',field)
			self.__query__['field']=','.join(field)
		return self

	def where(self,name,op,value):
		if not self.__query__['where'] ==False:
			self.__query__['where']=self.__query__['where']+' and '
			self.__query__['where']=self.__query__['where']+" `%s` %s %s "%(name,op,value)
		else:
			self.__query__['where']=" where  `%s` %s %s "%(name,op,value)
		return self

	def limit(self,num):
		sel.__query__['limit']=' limit %s '%num
		return self

	def orderBy(self,od):
		if isinstance(od,str):
			self.__query__['order']=' order by `%s` '%od
		else:
			self.__qeury__['order']=False
		return self

	def groupBy(self,gb):
		if isinstance(db,str):
			self.__query__['group']=' group by `%s` '%gb
		else:
			self.__query__['group']=False
		return self

	def having(self,name,op,value):
		self.__query__['having']=' having `%s` %s %s '%(name,op,value)
		return self
	
class User(Model):
	name=Column(String(20),primary_key=True,unique_key=True,null=False)
	age=Column(Int(1),default=12)
	email=Column(String(20),unique_key=True)

if __name__=='__main__':
	s=User()
	print(s.where('age','>',21).update('id',10))
