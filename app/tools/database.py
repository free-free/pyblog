#!/usr/bin/env python3.5

import os
import sys
import asyncio
import logging;logging.basicConfig(level=logging.ERROR)
from   tools.log import *
from   tools.config import Config
import re
import traceback
import sys
try:
	import aiomysql
except ImportError:
	logging.error('aiomysql module not Found')
	exit()
r'''
@asyncio.coroutine
def create_pool(loop,**kw):
	global pool
	pool=yield from aiomysql.create_pool(
				host=kw.get('host',Config.database.host),
				port=kw.get('port',Config.database.port),
				user=kw.get('user',Config.database.user),
				password=kw.get('password',Config.database.password),
				db=kw.get('database',Config.database.database),
				loop=loop
	)

@asyncio.coroutine
def select(sql,size=None):
	Log.info(sql)
	global pool
	with (yield from pool) as conn:
		cursor=yield from conn.cursor(aiomysql.DictCursor)
		yield from cursor.execute(sql)
		if size:
			records=yield from cursor.fetchmany(size)
		else:
			records=yield from cursor.fetchall()
		yield from cursor.close()
		return records

@asyncio.coroutine
def execute(sql,autocommit=True):
	Log.info(sql)
	with (yield from pool) as conn:
		if not autocommit:
			yield from conn.begin()
		try:
			cursor=yield from conn.cursor()
			yield from cursor.execute(sql)
			affectedrow=cursor.rowcount
			yield from cursor.close()
			if not autocommit:
				yield from conn.commit()
		except BaseException as e:
			if not autocommit:
				yield from conn.rollback()
			raise e
		return affectedrow			
'''
class DB(dict):
	_pool=""
	_loop=""
	def __init__(self,**kw):
		super(DB,self).__init__(**kw)
	@classmethod
	@asyncio.coroutine
	def createpool(cls,loop,**kw):
		cls._loop=loop
		cls._pool=yield from aiomysql.create_pool(
				host=kw.get('host',Config.database.host),
				port=kw.get('port',Config.database.port),
				user=kw.get('user',Config.database.user),
				password=kw.get('password',Config.database.password),
				db=kw.get('db',Config.database.database),
				loop=cls._loop
		)
	@asyncio.coroutine
	def _select(self,sql,size=None):
		Log.info(sql)
		with (yield from type(self)._pool) as conn:
			cursor=yield from conn.cursor(aiomysql.DictCursor)
			yield from cursor.execute(sql)
			yield from conn.commit()
			if size:
				records=yield from cursor.fetchmany(int(size))
			else:
				records=yield from cursor.fetchall()
			yield from cursor.close()
		return records
	@asyncio.coroutine
	def _execute(self,sql,autocommit=False):
		Log.info(sql)
		affectedrow=0
		with (yield from type(self)._pool) as conn:
			if autocommit:
				yield from conn.autocommit(True)
			else:
				yield from conn.begin()
			try:	
				cursor=yield from conn.cursor()
				yield from cursor.execute(sql)
			except Exception as e:
				yield from conn.rollback()
			finally:
				if not autocommit:
					yield from conn.commit()
				affectedrow=cursor.rowcount	
				yield from cursor.close()
		return affectedrow 
	@asyncio.coroutine	
	def connection(self,conn):
		type(self)._pool=yield from aiomysql.create_pool(
				host=Config.database.connection(conn).host,	
				port=Config.database.connection(conn).port,
				user=Config.database.connection(conn).user,
				password=Config.database.connection(conn).password,
				db=Config.database.connection(conn).database,	
				loop=type(self)._loop
				)
		return self
	def __fillparam(self,sql,args):
		if not args==None:
			if isinstance(args,list):
				args.reverse()
				def rep(obj):
					val=args.pop()
					if isinstance(val,str):
						return ' "'+val.strip()+'" '
					else:
						return ' '+str(val)+' '
				fullsql=re.sub('\?',rep,sql)
				return fullsql
			if isinstance(args,dict):
				def rep(obj):
					if isinstance(args[obj.group()[1:].strip()],str):
						return ' "'+args[obj.group()[1:].strip()]+'" '
					else:
						return ' '+str(args[obj.group()[1:].strip()])+' '
				fullsql=re.sub(':\w+\s?',rep,sql)
				return fullsql
		else:
			return sql
	def table(self,tablename):
		"""for query builder,table name must be set"""
		if tablename.strip()=='':
			Log.error('table name can\'t be empty')
			return False
		self['table']=tablename.strip()
		return self
	def getsql(self):	
		if 'fields' not in self or not self['fields']:
			self['fields']=' * '
		if 'table' not in self or not self['table']:
			Log.error('table name can\'t be empty')
			return False
		fullsql=' select %s from `%s` %s'%(self['fields'],self['table'],self['join'] if 'join' in self else '')
		self['join']=''
		self['fields']=''
		self['table']=''
		for item in ['where','order','limit','group','having']:
			if item in self:
				fullsql=fullsql+self[item]
				self[item]=''
		if 'union' in self:
			fullsql=fullsql+self['union']
			self['union']=''
		return fullsql
	def get(self):
		if 'fields' not in self or not self['fields']:
			self['fields']=' * '
		if 'table' not in self or not self['table']:
			Log.error('table name can\'t be empty')
			return False
		fullsql=' select %s from `%s` %s'%(self['fields'],self['table'],self['join'] if 'join' in self else '')
		self['join']=''
		self['fields']=''
		self['table']=''
		for item in ['where','order','limit','group','having']:
			if item in self:
				fullsql=fullsql+self[item]
				self[item]=''
		if 'union' in self:
			fullsql=fullsql+self['union']
			self['union']=''
		return fullsql
	def fields(self,args):
		fullsql=''
		if isinstance(args,list):
			def se(item):
				item=re.split('\.',item)
				if len(item)==2:
					if item[1].strip()=='*':
						return '%s.%s'%(item[0],item[1])
					else:
						return '%s.`%s`'%(item[0],item[1])
				else:
					return '`%s`'%item[0]
			fullsql=','.join(map(se,args))
		if isinstance(args,str):
			fullsql=args
		self['fields']=fullsql
		return self
	def select(self,sql=None,args=None):
		""" for raw select SQL """
		if not sql==None:
			if isinstance(sql,str):
				return self.__fillparam(sql,args)
		else:
			Log.error(" sql can't be null")
			return False
	def update(self,sql=None,args=None):
		"""for raw update SQL and query builder """
		if not sql==None:
			#for raw update SQL
			if isinstance(sql,str):
				return self.__fillparam(sql,args)
			#for qeury builder
			if isinstance(sql,dict):
				if 'table' not in self or not  self['table']:
					Log.error('table name must be set')
					self={}
					return False
				fullsql='update `%s` %s set '%(self['table'],self['join'])
				self['table']=''
				self['join']=''
				setitems=[]
				def se(item):
					item=re.split('\.',item)
					if len(item)==2:
						return '%s.`%s`'%(item[0],item[1])
					elif len(item)==1:
						return '`%s`'%item[0]
					else:
						raise KeyError()
				for k,v in sql.items():
					setitems.append(' %s=%s'%(se(k),'"'+v+'"' if isinstance(v,str) else str(v)))
				fullsql=fullsql+','.join(setitems)
				if 'where' in self:
					fullsql=fullsql+self['where']
					self['where']=''
				return fullsql
						
	def insert(self,sql=None,args=None):
		"""for raw insert SQL and  query builder"""
		if not sql==None:
			#for raw insert SQL
			if isinstance(sql,str):
				return self.__fillparam(sql,args)
			#for query builder,it's recommend to insert a large number of data set
			if isinstance(sql,list) and isinstance(sql[0],dict):
				fullsql=[]
				if 'table' not in self or not self['table']:
					Log.error('table name must be set')
					return False	
				for insert_item in sql:
					columns=','.join(map(lambda item:'`'+item+'`',insert_item.keys()))
					columns_value=','.join(map(lambda item:'"'+item+'"' if isinstance(item,str) else str(item),insert_item.values()))
					fullsql.append('insert into `%s`(%s) values(%s)'%(self['table'],columns,columns_value))
				self['table']=''
				return ';'.join(fullsql)
		
	def delete(self,sql=None,args=None):
		"""for raw delete SQL and query builder"""
		if not sql==None:
			#for raw delete SQL
			if isinstance(sql,str):
				return self.__fillparam(sql,args)
		else:
			#for query builder
			if 'table' not in self or not self['table']:
				Log.error('table name must be set')
				return False
			fullsql='delete from `%s` '%self['table']
			self['table']=''
			for item in ['where','order','limit','group','having']:
				if item in self:
					fullsql=fullsql+self[item]
					self[item]=''
			return fullsql
			
	def where(self,column,operator,value):
		#construct where condition and store it to self obj 
		standard_operator=set(['>','>=','<','<=','='])
		if str(operator).strip() not  in standard_operator:
			Log.error('operator is not correct in %s'%__file__)
			return False
		if 'where' in self and not self['where']=='':
			self['where']=self['where']+' and `%s`%s%s'%(column.strip(),str(operator).strip(),'"'+value+'"' if isinstance(value,str) else str(value))	
		else:
			self['where']=' where `%s`%s%s '%(str(column).strip(),str(operator).strip(),'"'+value.strip()+'"' if isinstance(value,str) else str(value))
		return self
	def orwhere(self,column,operator,value):
		standard_operator=set(['>','>=','<','<=','='])
		if 'where' in self and not self['where']=='':
			if str(operator).strip() not in standard_operator:
				Log.error('operator is not correct in %s'%__file__)
				return False
			self['where']=self['where']+' or `%s`%s%s'%(column.strip(),str(operator).strip(),'"'+value+'"' if isinstance(value,str) else str(value))
			return self
		return self
	def wherein(self,column,valtuple):
		if not isinstance(valtuple,tuple):
			Log.error('valtuple must be a tuple in %s'%__file__)
			raise ValueError('valtuple must be a tuple in %s'%__file__)
			return False
		if 'where' in self and not self['where']=='':
			self['where']=self['where']+' and `%s` in %s'%(column.strip(),valtuple)
		else:
			self['where']=' `%s` in %s'%(column.strip(),valtuple)
		return self
	def wherenotin(self,column,valtuple):
		if not isinstance(valtuple,tuple):
			Log.error("valtupe must be a tuple in %s"%__file__)
			raise ValueError('valtuple must be a tuple in %s'%__file__)
			return False
		if 'where' in self and not self['where']=='':
			self['where']=self['where']+' and `%s` not in %s'%(column.strip(),valtuple)
		else:
			self['where']=' where `%s` not in %s'%(column.strip(),valtuple)
		return self
	def wherebetween(self,column,valrange):
		if not isinstance(valrange,tuple):
			Log.error('valrange must be a tuple in %s'%__file__)
			raise ValueError('valrange must be a tuple in %s'%__file__)
			return False
		if 'where' in self and not self['where']=='':
			self['where']=self['where']+' and `%s`>=%s and `%s`<%s'%(column.strip(),valrange[0],column.strip(),valrange[-1])
		else:
			self['where']=' where `%s`>=%s and `%s`<%s'%(column.strip(),valrange[0],column.strip(),valrange[-1])
		return self
	def wherenotbetween(self,column,valrange):
		if not isinstance(valrange,tuple):
			Log.error("valrange must be a tuple in %s"%__file__)
			raise ValueError('valragne must be a tuple in %s'%__file__)
			return False
		if 'where' in self and not self['where'] =='':
			self['where']=self['where']+' and `%s`>%s or `%s`<%s'%(column.strip(),valrange[-1],column.strip(),valrange[0])
		else:
			self['where']='where `%s`>%s or `%s`<%s'%(column.strip(),valrange[-1],column.strip(),valrange[0])
		return self
	def join(self,innertable,column1,operator,column2):
		column1=re.split('\.',column1)
		column2=re.split('\.',column2)
		if len(column1)==2 and len(column1)==2:
			self['join']=' inner join `%s` on  %s.`%s` = %s.`%s` '%(innertable,column1[0],column1[1],column2[0],column2[1])
		elif len(column1)==1 and len(column2)==2:
			self['join']=' inner join `%s` on  `%s`=`%s` '%(innertable,column1[0],column2[0])
		else:
			return False
		return self
	def leftjoin(self,innertable,column1,operator,column2):
		column1=re.split('\.',column1)
		column2=re.split('\.',column2)
		if len(column1)==2 and len(column1)==2:
			self['join']=' left  join `%s` on %s.`%s` =%s.`%s` '%(innertable,column1[0],column1[1],column2[0],column2[1])
		elif len(column2)==1 and len(column2)==1:
			self['join']=' left join `%s` on `%s` = `%s` '%(innertable,column1[0],column2[0])
		else:
			return False
		return self
	def union(self,unionclosure):
		if isinstance(unionclosure,self.__class__):
			self['union']=' union %s '%unionclosure.getsql()
		return self
	def unionall(self,unionclosure):
		if isinstance(unionclosure,self.__class__):
			self['union']=' union all %s'%unionclosure.getsql()
		return self
	def count(self,column=''):
		if 'table' not in self or not self['table']:
			Log.error("table name can't be empty")
			return False
		fullsql=''
		if column.strip()=='':
			fullsql=fullsql+'select count(*) from `%s`'%self['table']
		else:
			fullsql=fullsql+'select count(`%s`) from `%s`'%(column.strip(),self['table'])
		self['table']=''
		return fullsql
	def max(self,column):
		if 'table' not in self or not self['table']:
			Log.error("table name can't be empty")
			return False
		if column=='' or column.strip()=='':
			Log.error(' column name can\'t be empty')
			return False
		fullsql='select max(`%s`) from `%s`'%(column.strip(),self['table'])
		self['table']=''
		return fullsql
	def min(self,column):
		if 'table' not in self or not self['table']:
			Log.error('table name can\'t be empty')
			return False
		if column=='' or column.strip()=='':
			Log.error('column name can\'t be empty')
			return False
		fullsql='select min(`%s`) from `%s`'%(column,self['table'])
		self['table']=''
		return fullsql
	def avg(self,column):
		if 'table' not in self or not self['table']:
			Log.error('table name can\'t be empty')
			return False
		if column=='' or column.strip()=='':
			Log.error('column name can\'t be empty')
			return False
		fullsql='select avg(`%s`) from `%s`'%(column,self['table'])
		self['table']=''
		return fullsql
	def sum(self,column):
		if 'table' not in self or not self['table']:
			Log.error('table name can\'t be empty')
			return False
		if column=='' or column.strip()=='':
			Log.error('column name can\'t be empty')
			return False
		fullsql='select sum(`%s`) from `%s`'%(column,self['table'])
		self['table']=''
		return fullsql
	def groupby(self,column):
		if column.strip()=='':
			Log.error('"group by" column is not given')
			return False
		self['group']=' group by `%s` '%column.strip()
		return self
	def orderby(self,column):
		if column.strip()=='' :
			Log.error('"order by" column is not given')
			return False
		self['order']=' order by `%s` '%str(column).strip()
		return self
	def limit(self,rownum):
		if rownum=='':
			Log.error('"limit" can\'t be empty')
			return False
		self['limit']=' limit %s '%int(rownum)
		return self
	def having(self,column,operator,value):
		standard_operator=set(['<','<=','>','>=','='])
		if str(operator).strip() not in standard_operator:
			Log.error('operator is not correct in %s'%__file__)
			return False
		self['having']=' having `%s`%s%s'%(str(column).strip(),str(operator).strip(),'"'+value.strip()+'"' if isinstance(value,str) else str(value))
		return self
	def __getattr__(self,key):
		if key in self:
			return self[key]
		return None
if __name__=='__main__':
	async def test(loop):
		#await create_pool(loop,db='pyblog',password='526114')
		await DB.createpool(loop)
		back=await DB()._execute('insert into `users`(`password`,`create_at`,`user_name`,`email`,`image`) values("950a97e2bed4fc741df8ee71d0d20ff5",1457709044.22579,"coderjell","18281573692@163.com","")')
		print(back)
	loop=asyncio.get_event_loop()
	loop.run_until_complete(asyncio.wait([test(loop)]))
	loop.run_forever()
	sys.exit(0)

	#db=DB()
	#db2=DB()
	#print(db.insert('insert into user(name,age,email) values(:name,:age,:email)',{'email':'2121','age':21,'name':'dsada'}))
	#print(db.update('update tb set name=:name where id=:id',{'id':1,'name':'xiaoming'}))
	#print(db.select('select * from user where id=:id',{'id':3}))
	#print(db.delete('delete from user where id=:id',{'id':30}))
	#print(db.table('user').insert([
	#{'name':'huanbiao','age':21,'email':'193213'},
	#{'name':'xiaohong','age':11,'email':'2121'},
	#{'name':'hujijdie','age':21,'email':'2121'}
	#]))
	#print(db.table('user').where('id','=',10).update({'id':1,'age':21}))
	#print(db.table('user'i).where('id','=',1).delete())
	#print(db.table('user').where('id','>',1).groupby('name').having('name','=','ghuangbiao').orderby('age').limit(1).get())
	#print(db.table(' user ').count('name'))
	#print(db.table('user').max('name'))
	#print(db.table('user').min('age'))
	#print(db.table('user').avg('id'))
	#print(db.table("user").sum('id'))
	#print(db.table('user').where('id','=',1).orwhere('name','=','huangiao').get())
	#print(db.table('need').fields('`name`,`age`,`id`').where('id','>',2).where('name','=','dede').get())
	#print(db.table("need").where('id','=',1).wherein('name',('de','D','f','f')).get())
	#print(db.table("user").wherenotin('id',('12','32','32','32')).where('name','=','huan').get())
	#print(db.table('user').wherebetween('id',(1,100)).fields(['name','age','email']).get())
	#print(db.table("user").wherenotbetween('id',(20,40)).fields(['name','age']).get())
	#print(db.table("users").fields(['users.id','needs.*']).join('needs','users.id','=','needs.solved_user_id').get())
	#print(db.table('users').join('needs','users.id','=','needs.solved_user_id').update({'is_solved':True}))
	#print(db.table('users').leftjoin('needs','users.id','=','needs.solved_user_id').get())
	#print(db.table('users').fields(['id','user_name']).union(db2.table('users').fields(['id','user_name']).where("id",'>',1)).get())
	
