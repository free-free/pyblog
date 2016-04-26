#-*- coding:utf-8 -*-
import datetime
import subprocess
import shlex
from tools.localization import Locale
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
	if not  hasattr(trans,'__locale__'):
		trans.__locale__=Locale()
	return trans.__locale__.translate(keys,**kw)

if __name__=='__main__':
	pass
	r'''print(trans("message:register.username",username="huangbiao",default="hello"))'''
