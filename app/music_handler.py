#-*- coding:utf-8 -*-
from tools.httptools import Route
from models import Music
from tools.config import Config
import logging
logging.basicConfig(level=logging.ERROR)
import time
import random
try:
	from qiniu import Auth
	import qiniu.config
except ImportError:
	logging.error("can't import 'qiniu' module")


@Route.get("/music")
def get_music_handler(app):
	m=Music()
	max_id=(yield from m.max('id'))[0]['id']
	if max_id<7:
		max_id=7
	rand_id=random.randrange(1,max_id-6)
	if rand_id>max_id:
		rand_id=max_id-6
	data=(yield from m.fields(['music_name','music_url']).where('id','>=',rand_id).limit(6).findall())
	ret={}
	ret['code']=200
	ret['msg']='ok'
	ret['type']=3
	ret['data']=data
	return ret

@Route.get("/music/token",auth=True)
def post_music_token_handler(app):
	auth=Auth(Config.filesystem.access_key,Config.filesystem.secret_key)
	policy={
		'callbackUrl':'http://localhost/music/callback',
		'callbackBody':'filename=$(fname)&filesize=$(fsize)',
	}
	token=auth.upload_token(Config.filesystem.bucket_name,'',0,policy)
	return {"_token":token}
@Route.get("/music/callback")
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
		return {'code':200,'msg':'o:ok'}
	return {'code':300,'msg':"bad"}
