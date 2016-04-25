#-*- coding:utf-8 -*-
import os
import json
from tools.config import Config
class LocaleProxyer(dict):
	_locale_file_dir=None
	_locale_files_content={}
	def __init__(self,locale_file_dir):
		assert isinstance(locale_file_dir,str)
		if type(self)._locale_file_dir !=os.path.abspath(locale_file_dir):		
			type(self)._locale_file_dir=os.path.abspath(locale_file_dir)
	def get_locale_item(self,filename,item):
		items=item.split('.')
		absfilename=os.path.join(self._locale_file_dir,filename)
		if absfilename not in self:
			if os.path.exists(absfilename):
				with open(absfilename) as f:
					self[absfilename]=json.load(f)
		item_content=self[absfilename]
		for item_name in items:
			try:
				tmp_content=item_content[item_name]
			except Exception:
				item_content=None
			else:
				item_content=tmp_content
		return item_content
	
class Locale(object):
	_locale_dir=os.path.abspath('../locale')
	_locale_file_suffix='.py'
	def __init__(self,locale_proxyer=LocaleProxyer):
		self._locale_proxyer=locale_proxyer(os.path.join(self._locale_dir,Config.app.locale))
	def translate(self,key):
		key=key.split(':')
		locale_filename=key[0]+self._locale_file_suffix
		locale_items=key[1]
		return self._locale_proxyer.get_locale_item(locale_filename,locale_items)

if __name__=='__main__':
	l=Locale()
	print(l.translate('message:register.password'))
	print(l.translate('message:login.password'))
	#print(LocaleProxyer('../locale/chinese').get_locale_item('message.py','login.email'))

	
	


