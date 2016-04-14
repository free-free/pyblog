#-*- coding:utf-8 -*-
from tools.taskqueue import Task
import re

class MailAddress(object):
	_mail_regexp=r'^[0-9\w]+[\.0-9\w]+@[0-9\w]+(\.[\w0-9]+)+$'
	def __init__(self,mail_address=None):
		if mail_address:
			self._mail_address=mail_address
		else:
			self._mail_address=''
	def __get__(self,obj,ownclass):
		return self._mail_address
	def __set__(self,obj,value):
		if not re.match(self._mail_regexp,value):
			raise ValueError("mail address is not correct address")
		self._main_address=value	
class Job(object):
	def __init__(self,tries=None,*,tasker=Task):
		if tries:
			self._tries=tries
		else:
			self._tries=3
		self._tasker=tasker
	def set_tries(self,tries):
		self._tries=tries
class MailJob(Job):
	_sender=MailAddress()
	_receiver=MailAddress()
	def send(self):
		content={}
		content['receiver']=self._receiver
		content['title']=self._title
		content['sender']=self._sender
		content['main']=self._main
		self._tasker('mail',self._tries,content).start('mail')
	def set_mail_receiver(self,receiver):
		self._receiver=receiver
	def set_mail_title(self,title):
		self._title=title
	def set_mail_sender(self,sender):
		self._sender=sender
	def set_mail_main(self,main):
		self._main=main
	@property
	def main(self):
		return self._main
	@main.setter
	def main(self,main):
		self._main=main
	@property
	def title(self):
		return self._title
	@title.setter
	def title(self,title):
		self._title=title
	@property
	def sender(self):
		return self._sender
	@sender.setter
	def sender(self,sender):
		self._sender=sender
	@property
	def receiver(self):
		return self._receiver
	@receiver.setter
	def receiver(self,receiver):
		self._receiver=receiver
	
if __name__=='__main__':
	mail=MailJob()
	mail.title='hello'
	mail.main='shabi'
	mail.sender='18281573692@163.com'
	mail.receiver='19941222hb@gmail.com'
	mail.send()
