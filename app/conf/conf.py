#-*- coding:utf-8 -*-
database={
	'default':'mysql',
	'connections':{
		'mysql':{
			'host':'127.0.0.1',
			'user':'root',
			'port':3306,
			'password':'526114',
			'database':'pyblog'
		},
		'mongodb':{
			'host':'127.0.0.1',
			'user':'xxxx',
			'port':27017,
			'auth':'526114'
		}
	}
}
session={
	'default':'file',
	'drivers':{
		'file':{
			'session_dir':'/tmp/session/',
			'expire_file':'session_expire',
			'expire':0
		},
		'redis':{
			'host':'localhost',
			'port':6379,
			'db':0,
			'expire':0
		},	
		'mongo':{
			'host':'localhost',
			'port':27017,
			'db':'session',
			'collection':'session',
			'expire':0
		}
	}
}
