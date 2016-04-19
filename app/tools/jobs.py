#-*- coding:utf-8 -*-
from tools.taskqueue import Task,TaskProcessionReminder
import re
from tools.asynctaskqueue import AsyncTask
import asyncio

class MailAddress(object):
	_mail_regexp=r'^[0-9\w]+[\.0-9\w]+@[0-9\w]+(\.[\w0-9]+)+$'
	def __init__(self,mail_address=None):
		self._mail_address=''
		if mail_address:
			self._mail_address=mail_address
	def __get__(self,obj,ownclass):
		return self._mail_address
	def __set__(self,obj,value):
		if not re.match(self._mail_regexp,value):
			raise ValueError("mail address is not correct address")
		self._mail_address=value
class Job(object):
	def __init__(self,tries=None,*,tasker=Task,reminder=TaskProcessionReminder):
		if tries:
			self._tries=tries
		else:
			self._tries=3
		self._tasker=tasker
		self._reminder=reminder
	def set_tries(self,tries):
		self._tries=tries
class MailJob(Job):
	_sender=MailAddress()
	_receiver=MailAddress()
	def send(self):
		content={}
		content['receiver']=self._receiver
		content['subject']=self._subject
		content['sender']=self._sender
		content['main']=self._main
		self._tasker('mail',self._tries,content).start('mail')
		self._reminder('127.0.0.1',9999).remind('mail')
	def set_mail_receiver(self,receiver):
		self._receiver=receiver
	def set_mail_subject(self,subject):
		self._subject=subject
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
	def subject(self):
		return self._subject
	@subject.setter
	def subject(self,subject):
		self._subject=subject
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
class AsyncMailJob(MailJob):
	def __init__(self,loop,tries,tasker=AsyncTask):
		self._loop=loop
		super(AsyncMailJob,self).__init__(tries,tasker=tasker)
	@asyncio.coroutine
	def send(self):
		content={}
		content['receiver']=self._receiver
		content['subject']=self._subject
		content['sender']=self._sender
		content['main']=self._main		
		yield from self._tasker('mail',self._tries,content,self._loop).start()
		

if __name__=='__main__':
	loop=asyncio.get_event_loop()
	mail=AsyncMailJob(loop,3)
	mail.subject='hello'
	mail.main='john shabi'
	mail.sender='18281573692@163.com'
	mail.receiver='19941222hb@gmail.com'
	loop.run_until_complete(mail.send())
	loop.close()
