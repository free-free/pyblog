#!/usr/bin/env python3.5
# -*- coding:utf-8 -*-
import argparse
import sys
from tools.taskqueue import TaskProcessionReceiver,QueuePayloadRouter,MailExecutor
from tools.dbautocreate import DBBuilder
def main():
	if len(sys.argv)==1:
		sys.argv.append('--help')
	parser=argparse.ArgumentParser()
	parser.add_argument('--queue',help="run queue processor")
	parser.add_argument("--port",help="queue processor listening port ",default=9999)
	parser.add_argument("--host",help="queue processor runining host",default="localhost")
	parser.add_argument('--dbbuild',help="build database")
	args=parser.parse_args()
	if args.queue:
		if args.queue.lower() =='start':
			QueuePayloadRouter.register_executor(mail=MailExecutor)
			TaskProcessionReceiver(args.host,int(args.port)).listen()
	elif args.dbbuild:
		if args.dbbuild.lower()=='start':
			DBBuilder.build()
			print("build database sucessfully!")
if __name__=='__main__':
	main()
