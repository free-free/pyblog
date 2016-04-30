#-*- coding:utf-8 -*-
import datetime
import subprocess
import shlex
from tools.localization import Locale
from tools.taskqueue import Task
def execute_shell_cmd(cmd,timeout=60,bufsize=4096):
	assert isinstance(cmd,str)
	cmd=shlex.split(cmd)
	sub=subprocess.Popen(cmd,stdin=subprocess.PIPE,bufsize=bufsize)
	end_time=datetime.datetime.now()+datetime.timedelta(seconds=timeout)
	while sub.poll() is None:
		if timeout:
			if end_time<datetime.datetime.now():
				raise Exception("execution shell command '%s' failed"%(cmd))
	return sub.returncode
def shell_echo(echo_string,color):
	COLOR_CODE={
		'black':'0;30m',
		'red':'0;31m',
		'green':'0;32m',
		'brown':'0;33m',
		'blue':'0;34m'
	}
	cmd='echo -e "\e[{color}{string}\e[m"'.format(color=COLOR_CODE.get(color.lower(),'0;30m'),string=echo_string)
	execute_shell_cmd(cmd)

def locale_translate(keys,**kw):
	if not  hasattr(locale_translate,'__locale__'):
		locale_translate.__locale__=Locale()
	return locale_translate.__locale__.translate(keys,**kw)

def task(task_type,tries,content):
	if not hasattr(task,'__task_instance__'):
		task.__task_instance=Task(task_type,tries,content)
	else:
		task.__task_instance.refresh_task(task_type,tries,content)
	task.__task_instance.start()
if __name__=='__main__':
	pass
	r'''print(trans("message:register.username",username="huangbiao",default="hello"))'''
