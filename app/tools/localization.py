#-*- coding:utf-8 -*-
import os
import json
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
		if filename not in self._locale_files_content:
			if os.path.exists(absfilename):
				with open(absfilename) as f:
					type(self)._locale_files_content[absfilename]=json.load(f)
		item_content=self._locale_files_content[absfilename]
		for item_name in items:
			try:
				tmp_content=item_content[item_name]
			except Exception:
				item_content=None
			else:
				item_content=tmp_content
		return item_content
	
class Locale(object):
	def __init__(self,locale_proxyer=LocaleProxyer):
		pass
	def translate(self,key):
		pass

if __name__=='__main__':
	print(LocaleProxyer('../locale/chinese').get_locale_item('message.py','login.email'))

	
	


