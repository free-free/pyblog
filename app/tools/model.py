#!/usr/bin/env python3

import os

from tools.log import *
from tools.field import *
from tools.column import *
from tools.database import *
from collections import OrderedDict
import hashlib
try:
	import aiomysql
except ImportError:
	info=r" 'aiomysql' module  not Found"
	Log.error(info)
	raise ImportError(info)

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
		autoIncrement=[]
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
				if c_type.constraints['auto_increment']==True:
					autoIncrement.append(c_name)
				if not c_type.constraints['default']=='':
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
		attrs['__auto_increment__']=autoIncrement
		attrs['__query__']=OrderedDict(dict({'where':'','order':'','limit':'','group':'','having':''}))
		attrs['__fields__']=dict({'fields':' * ','values':''})
		return type.__new__(cls,name,bases,attrs)



class Model(dict,metaclass=ModelMetaclass):
	def __init__(self,**kw):
		columns=dict()
		type(self).db=DB()
		for column_name in self.__columns__:
			columns[column_name]=self.__columns__[column_name]['constraints']['default']
		for  name,value in kw.items():
			if name not in self.__columns__.keys():
				info=r"'%s' has no column '%s' "%(self.__class__.__name__,name)
				Log.error(info)
				raise AttributeError(info)
			else:
				columns[name]=value
		super(Model,self).__init__(self,**columns)
	def __setattr__(self,key,value):
		if key in self.__columns__.keys():
			self[key]=value
		else:
			info=r"'%s' has no column '%s' "%(self.__class__.__name__,key)
			Log.warning(info)

	def __getattr__(self,key):
		if key in self:
			return self[key]
	@asyncio.coroutine
	def findall(self):		
		sql='select %s from `%s`'%(self.__fields__['fields'],self.__table__)
		self.__fields__['fields']=' * '
		for k in ['where','order','limit','group','having']:
			sql=sql+' %s '%self.__query__[k]
			self.__query__[k]=''
		#records=yield from select(sql)
		records=yield from self.db._select(sql)
		return [type(self)(**k) for k in records]
	@asyncio.coroutine
	def findone(self,n=None):
		sql='select %s from `%s` '%(self.__fields__['fields'],self.__table__)
		self.__fields__['fields']=' * '
		if not n==None:
			sql=sql+'where `%s` =%s'%(self.__primary_key__,n)
		else:
			self.limit(1)
			for k in ['where','order','limit','group','having']:
				sql=sql+self.__query__[k]
				self.__query__[k]=''
		#record=yield from select(sql)
		record=yield from self.db._select(sql)
		return type(self)(**record[0])
	@asyncio.coroutine
	def update(self,args):
		if not isinstance(args,dict):
			raise ValueError
		for k in args.keys():
			if k not in self.__columns__.keys():
				info="'%s' has no column '%s'"%(self.__class__.__name__,k)
				Log.error(info)
				raise AttributeError(info)
		setitems=[]
		for k,v in args.items():
			setitems.append('`%s`=%s'%(k,v))	
		sql='update `%s` '%self.__table__+' set %s '%(','.join(setitems))
		if self.__query__['where']:
			sql=sql+self.__query__['where']
			self.__query__['where']=''
		#return (yield from execute(sql))	
		return (yield from self.db._execute(sql))
	@asyncio.coroutine
	def save(self):
		for cname in self.__columns__.keys():
			if cname in self.__not_null__ and cname in self and self[cname]=='' and cname not in self.__auto_increment__:
				info="'%s' column can't be null "%cname
				Log.error(info)
				raise ValueError(info)
			if cname not in self.keys() and cname in self.__not__null__:
				info="'%s'  column can't be null"%cname
				Log.error(info)
				raise ValueError(info)
		if self.__fields__['fields']==' * ':
			self.__fields__['fields']=' '
		sql=''
		if self.__fields__['values']=='':
			insertcolumns=[]
			insertvalues=[]
			for cname in self.__columns__.keys():
				if cname  in self.__auto_increment__ and  self[cname]=='':
					continue
				insertcolumns.append('`'+cname+'`')
				if isinstance(self[cname],str):
					insertvalues.append('"'+self[cname]+'"')
				else:
					insertvalues.append(str(self[cname]))
			sql=sql+'insert into `%s`(%s) values(%s)'%(self.__table__,','.join(insertcolumns),','.join(insertvalues))
		else:
			sql=sql+'insert into `%s` %s '%(self.__table__,self.__fields__['fields'])
			sql=sql+self.__fields__['values']
			self.__fields__['values']=''
		self.__fields__['fields']=' * '
		for k in ['where','order','limit','group','having']:
			sql=sql+self.__query__[k]
			self.__query__[k]=''
		#result=yield from execute(sql)
		result=yield from self.db._execute(sql)
		return result
	@asyncio.coroutine
	def delete(self,n=None):
		sql='delete from `%s`'%self.__table__
		if not n==None and self.__query__['where']=='':
			sql=sql+' where `%s` = %s '%(self.__primary_key__,n)
		else:
			if self.__query__['where']:
				sql=sql+self.__query__['where']
				self.__query__['where']=''
		#return (yield from execute(sql))
		return (yield from self.db._execute(sql))
	@asyncio.coroutine
	def destroy(self,l):
		sql=''
		if isinstance(l,list):
			sql='delet from `%s` where '%self.__table__
			l=map(lambda x:'`%s` = %s'%(self.__primary_key__,x),l)
			sql=sql+' or '.join(l)
		#return (yield from execute(sql))
		return (yield from self.db._execute(sql))
	def fields(self,field):
		if isinstance(field,list):
			for cname in field:
				if  cname not  in self.__columns__.keys():
					raise AttributeError(" '%s' has not column '%s' "%(self.__class__.__name__,cname))
			values=[]
			fields=[]
			for cname in field:
				fields.append('`'+cname+'`')
				if isinstance(self[cname],str):
					values.append('"'+self[cname]+'"')
				else:		
					values.append(str(self[cname]))
			self.__fields__['fields']='('
			self.__fields__['fields']=self.__fields__['fields']+','.join(fields)
			self.__fields__['fields']=self.__fields__['fields']+')'
			self.__fields__['values']=' values('
			self.__fields__['values']=self.__fields__['values']+','.join(values)+') '
		return self

	def where(self,name,op,value):
		if name not in self.__columns__.keys():
			raise AttributeError("'%s' has no column '%s'"%(self.__class__.__name__,name))
		if not self.__query__['where'] =='':
			self.__query__['where']=self.__query__['where']+' and '
			self.__query__['where']=self.__query__['where']+" `%s` %s %s "%(name,op,'"'+value+'"' if isinstance(value,str)else str(value))
		else:
			self.__query__['where']="where `%s` %s %s "%(name,op,'"'+value+'"' if isinstance(value,str)else str(value))
		return self

	def limit(self,num):
		self.__query__['limit']='limit %s '%num
		return self

	def orderby(self,od):
		if od not in self.__columns__.keys():
			raise AttributeError("'%s' has no column '%s'"%(self.__class__.__name__,od))
		if isinstance(od,str):
			self.__query__['order']='order by `%s` '%od
		else:
			self.__qeury__['order']=''
		return self

	def groupby(self,gb):
		if gb not in self.__columns__.keys():
			raise AttributeError("'%s' has no column '%s'"%(self.__class__.__name__,gb))
		if isinstance(gb,str):
			self.__query__['group']='group by `%s` '%gb
		else:
			self.__query__['group']=''
		return self

	def having(self,name,op,value):
		if name not in self.__columns__.keys():
			raise AttributeError("'%s' has no column '%s'"%(self.__class__.__name__,name))
		self.__query__['having']='having `%s` %s %s '%(name,op,value)
		return self
		
class User(Model):
	name=Column(String(20),primary_key=True,unique_key=True)
	age=Column(Int(1),default=12)
	email=Column(String(20),unique_key=True)
if __name__=='__main__':
	pass
