#!/usr/bin/env python3.5
# -*- coding:utf-8 -*-
import argparse
import sys
import subprocess
import datetime
import shlex
from tools.taskqueue import TaskProcessionReceiver,QueuePayloadRouter,MailExecutor
from tools.dbautocreate import DBBuilder
def execute_shell_cmd(cmd):
	assert isinstance(cmd,str)
	cmd=shlex.split(cmd)
	sub=subprocess.Popen(cmd,stdin=subprocess.PIPE,bufsize=4096)
	timeout=60
	end_time=datetime.datetime.now()+datetime.timedelta(seconds=timeout)
	while sub.poll() is None:
		if timeout:
			if end_time<datetime.datetime.now():
				raise Exception("execution shell command '%s' timeout"%cmd)
	return (sub.returncode)
def shell_echo(string,color):
	color_code={
		'red':'0;31m',
		'green':'0;32m',
		'blue':'0;34m',
		'brown':'0;33m'
	}
	cmd='echo -e "\e[{color} {string} \e[m"'.format(color=color_code.get(color.lower(),'0;30m'),string=string)
	execute_shell_cmd(cmd)

def main():
	if len(sys.argv)==1:
		sys.argv.append('--help')
	parser=argparse.ArgumentParser()
	parser.add_argument('--queue',help="run queue processor")
	parser.add_argument("--port",help="queue processor listening port ",default=9999)
	parser.add_argument("--host",help="queue processor runining host",default="localhost")
	parser.add_argument('--dbbuild',help="build database",default="start")
	args=parser.parse_args()
	if args.queue:
		if args.queue.lower() =='start':
			QueuePayloadRouter.register_executor(mail=MailExecutor)
			TaskProcessionReceiver(args.host,int(args.port)).listen()
	elif args.dbbuild:
		if args.dbbuild.lower()=='start':
			DBBuilder.build()
			shell_echo("build database sucessfully!",'green')
if __name__=='__main__':
	main()
