#!/usr/bin/env python3.5
# -*- coding:utf-8 -*-
import os
try:
    from jinja2 import Environment,FileSystemLoader
except ImportError:
    raise ImportError("Can't import jinja2 module")

class Template(object):
	def __init__(self,template):
		pass	
	@classmethod
	def render(cls,template,**kw):
		res={'__template__':template}
		for k,v in kw.items():
			res[k]=v
		return res
	@classmethod
	def init(self,app,**kw):
		options=dict(
			autoescape=kw.get("autoescape",True),
			block_start_string=kw.get("block_start_string",'{%'),
			block_end_string=kw.get("block_end_string",'%}'),
			variable_start_string=kw.get("variable_start_string",'{{'),
			variable_end_string=kw.get("varibale_end_string",'}}'),
			auto_reload=kw.get("auto_reload",True)
		)
		path=os.path.join(os.path.dirname(os.path.dirname(__file__)),'templates')
		env=Environment(loader=FileSystemLoader(path),**options)
		app['__templating__']=env
	
