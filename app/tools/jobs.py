#-*- coding:utf-8 -*-
from tools.taskqueue import Task
import re

class MailAddress(object):
	_mail_regexp=r'^[0-9\w]+[\.0-9\w]+@[0-9\w]+(\.[\w0-9]+)+$'
	def __init__(self):
		self._mail_address=''
	def __get__(self,obj,ownclass):
		return self._mail_address
	def __set__(self,obj,value):
		if not re.match(self._mail_regexp,value):
			raise ValueError("mail address is not correct address")
		self._main_address=value	
class MailJob(object):
	_sender=MailAddress()
	_receiver=MailAddress()
	def __init__(self,tasker=Task):
		self._tasker=task
		self._content=''
		self._tries=3
	def send_mail(self):
		self._tasker('mail',self._tries,self._content).start('mail')
	def set_mail_receiver(self,receiver):
		self._receiver=receiver
	def set_mail_title(self,title):
		self._title=title
	def set_mail_sender(self,sender):
		self._sender=sender
	def set_mail_main(self,main):
		self._main=main
	def set_mail_tries(self,tries):
		self._tries=tries
	
