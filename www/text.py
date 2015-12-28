#!/usr/bin/env python3
from tools.orm import *
from tools.log import *
class U(Model):
	name=Column(String(20),primary_key=True)
	email=Column(String(20),uniqeu_key=True)
	

if __name__=='__main__':
	m=U(name='huangiao',email='199412212j')
	Log.info(m.where('name','>','huangbiao').field(['name','age']).findAll())
