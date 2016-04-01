#!/usr/bin/env python3.5

from tools.config import Config
import logging
logging.basicConfig(level=logging.ERROR)
from app.models import *
try:
	import MySQLdb
except ImportError:
	logging.error("can't import 'MySQLdb' module")

class DBAutoBuilder(object):
	def __init__(self):
		pass
	def run(self):
		pass

class MysqlAutoBuilder(DBAutoBuilder):
	def __new__(cls,*args,**kw):
		if not hasattr(cls,'_instance'):
			cls._instance=super().__new__(cls)
		return cls._instance
	def __init__(self,model):
		self._table=model.__table__
		self._fields=model.__columns__
		self._sql=''
		if not hasattr(type(self),'_conn'):
			type(self)._conn=MySQLdb.connect(db=Config.database.database,
						user=Config.database.user,
						host=Config.database.host,
						passwd=Config.database.password)
		self._exists_tables=self._get_db_all_tables()
		if self._table in self._exists_tables:
			self._delete_db_table(self._table)
	def _delete_db_table(self,table):
		cursor=self._conn.cursor()
		ret=cursor.execute("drop table %s;"%table)
		cursor.close()
		return ret
	def _get_db_all_tables(self):
		cursor=self._conn.cursor()
		cursor.execute("show tables;")
		alltables =cursor.fetchall()
		cursor.close()
		tables=[]
		for table in alltables:
			tables.append(table[0])
		print (tables)
		return tables
	def _create_table_sql(self):
		self._sql='CREATE TABLE `%s` ('%self._table
		for field_name,field in self._fields.items():
			self._sql+=' `%s` '%field_name
			self._sql+=field['type']
			if field['constraints']['primary_key']:
				self._sql+=' PRIMARY KEY'
			if field['constraints']['auto_increment']:
				self._sql+=' AUTO_INCREMENT'
			if field['constraints']['unique_key']:
				self._sql+=' UNIQUE KEY'
			if field['constraints']['null']:
				self._sql+=' NOT NULL '
			if field['constraints']['default']:
				self._sql+=' default "'+str(field['constraints']['default'])+'"'
			self._sql+=', '
		self._sql=self._sql[:self._sql.rindex(',')]
		self._sql+=' ) charset utf8;'
		return self._sql
	def run(self):
		self._create_table_sql()
		cursor=type(self)._conn.cursor()
		cursor.execute(self._sql)
		cursor.close()
		type(self)._conn.commit()
class DBBuilder(object):
	_all_builders={"mysql":MysqlAutoBuilder}
	_models=[User(),Article(),Category(),Comment(),Music(),Image(),Share(),Book()]
	def __init__(self):
		pass
	@classmethod
	def build(self):
		default_connection=Config.database.connection_name
		for model in self._models:
			self._all_builders[default_connection](model).run()
if __name__=='__main__':
	DBBuilder.build()

	


