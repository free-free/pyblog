#-*- coding:utf-8 -*-
from tools.httptools import Route
from models import Music

@Route.get("/music")
def get_music_handler(app):
	ret={};
	ret['code']=200
	ret['msg']='ok'
	ret['type']=3
	ret['data']=[
	 {'music_name':'CountrintStars','music_url':'http://7xs7oc.com1.z0.glb.clouddn.com/music%2FJason%20Chen%20-%20Counting%20Stars.mp3'},
	]
	return ret
@Route.post("/music")
def post_music_handler(app):
	return 'ok'

