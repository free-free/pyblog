#-*- coding:utf-8 -*-

import smtplib
from email.mime.text import MIMEText
from email.header import Header
from tools.config import Config
class MailSender(object):
	def __init__(self,email_content,*,host=None,port=None,username=None,password=None,mail_server=smtplib.SMTP):
		self._mail_content=email_content
		self._host=host or Config.mail.host
		self._port=port or Config.mail.port
		self._username=username or Config.mail.user
		self._password=password or Config.mail.password
		self._mail_server=mail_server
	def get_mail_subject(self):
		return self._mail_content.get('subject')
	def get_mail_sender(self):
		return self._mail_content.get('sender')
	def get_mail_receiver(self):
		return self._mail_content.get('receiver')
	def get_mail_main(self):
		return self._mail_content.get('main')
	def mail_encapsulate(self):
		msg=MIMEText(self.get_mail_main(),'html','utf-8')
		msg['From']=self.get_mail_sender()
		msg['To']=self.get_mail_receiver()
		msg['subject']=Header(self.get_mail_subject(),'utf-8').encode()
		return msg
	def send_mail(self):
		server=self._mail_server(self._host,self._port)
		server.starttls()
		server.login(self._username,self._password)
		server.sendmail(self.get_mail_sender(),self.get_mail_receiver(),self.mail_encapsulate().as_string())
		server.quit()

