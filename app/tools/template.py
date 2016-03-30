#!/usr/bin/env python3.5
# -*- coding:utf-8 -*-
import os
from app.config import Config
try:
    from jinja2 import Environment,FileSystemLoader
except ImportError:
    raise ImportError("Can't import jinja2 module")

class Template(object):
	def __init__(self,template):
		self._template=template
	def render(self,**kw):
		res={'__template__':self._template}
		for k,v in kw.items():
			res[k]=v
		return res
	@classmethod
	def init(cls,app,**kw):
		options=dict(
			autoescape=kw.get("autoescape",True),
			block_start_string=kw.get("block_start_string",'{%'),
			block_end_string=kw.get("block_end_string",'%}'),
			variable_start_string=kw.get("variable_start_string",'{{'),
			variable_end_string=kw.get("varibale_end_string",'}}'),
			auto_reload=kw.get("auto_reload",True)
		)
		template_path=Config.app.template_path
		if template_path.find('.')==0:
			template_path=os.path.join(os.path.dirname(os.path.dirname(__file__)),template_path)
		env=Environment(loader=FileSystemLoader(template_path),**options)
		app['__templating__']=env
	
