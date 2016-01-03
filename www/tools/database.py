#!/usr/bin/env python3
import os
import sys
os.sys.path.append(os.path.join(os.path.dirname(__file__),'../'))
import asyncio
import logging;logging.basicConfig(level=logging.ERROR)
from   tools.log import *
import re
import traceback
import sys
try:
	import aiomysql
except Exception:
	logging.error('aiomysql module not Found')
	exit()
@asyncio.coroutine
def create_pool(loop,**kw):
	global pool
	pool=yield from aiomysql.create_pool(
				host=kw.get('host','localhost'),
				port=kw.get('port',3306),
				user=kw.get('user','root'),
				password=kw['password'],
				db=kw['db'],
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
			conn.begin()
		try:
			cursor=yield from conn.cursor()
			yield from cursor.execute(sql)
			affectedrow=cursor.rowcount
			yield from cursor.close()
			if not autocommit:
				conn.commit()
		except BaseException as e:
			if not autocommit:
				conn.rollback()
			raise e
		return affectedrow			

class DB(dict):
	__connectionPool=""
	def __init__(self,**kw):
		super().__init__(**kw)
	@classmethod
	def createpool(cls,loop,**kw):
		cls.__connectionPool=yield from aiomysql.create_pool(
				host=kw.get('host','localhost'),
				port=kw.get('port',3306),
				user=kw.get('user','root'),
				password=kw.get('password'),
				db=kw.get('db','test'),
				loop=loop
		)	
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
	def get(self):
		if 'fields' not in self or not self['fields']:
			self['fields']=' * '
		if 'table' not in self or not self['table']:
			Log.error('table name can\'t be empty')
			return False
		fullsql=' select %s from `%s` '%(self['fields'],self['table'])
		self['fields']=''
		self['table']=''
		for item in ['where','order','limit','group','having']:
			fullsql=fullsql+self[item]
			self[item]=''
		return fullsql
	def fields(self,args):
		fullsql=''
		if isinstance(args,list):
			fullsql=','.join(map(lambda x:'`'+x+'`',args))
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
				fullsql='update `%s` set '%self['table']
				self['table']=''
				setitems=[]
				for k,v in sql.items():
					setitems.append(' `%s`=%s'%(k,'"'+v+'"' if isinstance(v,str) else str(v)))
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
		self['where']=' where `%s`%s%s '%(str(column).strip(),str(operator).strip(),'"'+value.strip()+'"' if isinstance(value,str) else str(value))
		return self
	def orwhere(self,column,operator,value):
		pass
	def wherein(self,column,vallist):
		pass
	def wherenotin(self,column,vallist):
		pass
	def wherebetween(self,column,valrange):
		pass
	def wherenotbetween(self,column,valrange):
		pass
	def join(self,tableName,column1,operator,column2):
		pass
	def leftjoin(self,tableName,column1,operator,column2):
		pass
	def union(self):
		pass
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
	"""
	async def test(loop):
		await create_pool(loop,db='pyblog',password='526114')
		re=await select('desc users')
		print(re)
	loop=asyncio.get_event_loop()
	loop.run_until_complete(asyncio.wait([test(loop)]))
	loop.close()
	sys.exit(0)
	"""
	db=DB()
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
	print(db.table("user").sum('id'))
