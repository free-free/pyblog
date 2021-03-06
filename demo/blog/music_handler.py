#-*- coding:utf-8 -*-
from pyblog.httptools import Route
from models import Music
from pyblog.config import Config
import logging
logging.basicConfig(level=logging.ERROR)
import time
import random
try:
	from qiniu import Auth
	import qiniu.config
except ImportError:
	logging.error("can't import 'qiniu' module")

@Route.get("/api/music")
def get_music_handler(app):
	max_id_arr=(yield from Music().max('id'))
	if len(max_id_arr)==0:
		max_id=8
	else:
		max_id=max_id_arr[0].get('id')
	if  not max_id or max_id<7:
		max_id=8
	rand_id=random.randrange(1,max_id-6)
	data=(yield from Music().fields({'music_name':'title','music_url':'url'}).where('id','>=',rand_id).limit(6).findall())
	ret=dict()
	ret['code']=200
	ret['msg']='ok'
	ret['type']=3
	ret['data']=data
	return ret
@Route.get("/api/music/token",auth=True)
def post_music_token_handler(app):
	auth=Auth(Config.filesystem.access_key,Config.filesystem.secret_key)
	policy={
		'callbackUrl':'http://localhost/music/callback',
		'callbackBody':'filename=$(fname)&filesize=$(fsize)&key=$(key)',
	}
	token=auth.upload_token(Config.filesystem.bucket_name,'',0,policy)
	return {"_token":token}
@Route.get("/api/music/callback")
def post_music_callback_handler(app):
	m=Music()
	m.uid=1
	m.upload_at=str(time.time())
	m.type_id=1
	m.belong_id=1
	m.music_name='CountingStar'
	m.music_url='http://7xs7oc.com1.z0.glb.clouddn.com/music%2FJason%20Chen%20-%20Counting%20Stars.mp3'
	ret=(yield from m.save())
	if ret:
		return {'code':200,'msg':'ok'}
	return {'code':300,'msg':"bad"}
