#-*- coding:utf-8 -*-
import logging
logging.basicConfig(level=logging.ERROR)
from tools.config import Config
try:
	from qiniu import Auth,put_file,etag,urlsafe_base64_encode,BucketManager
	import qiniu.config
except ImportError:
	logging.error("can't import 'qiniu' module")
	exit(-1)

class QiniuFileSystemAdapter(object):
	__slots__=('__access_key','__secret_key','__auth','__bucket','__file_info_cache')
	def __init__(self,access_key,secret_key,*args,**kw):
		self.__access_key=access_key
		self.__secret_key=secret_key
		self.__auth=Auth(self.__access_key,self.__secret_key)
		self.__bucket=BucketManager(self.__auth)
		self.__file_info_cache={}
	def __gen_upload_token(self,bucket,key,expire=3600,policy=None):
		assert isinstance(bucket,str)
		assert isinstance(key,str)
		assert isinstance(expire,int)
		assert isinstance(policy,(str,dict,type(None)))
		if policy:
			token=self.__auth.upload_token(bucket,key,expire,policy)
		else:
			token=self.__auth.upload_token(bucket,key,expire)
		return token
	def upload_token(self,bucket,key,expire=3600,policy=None):
		return self.__gen_upload_token(bucket,key,expire,policy)
	def upload(self,token,key,local_file):
		ret,info=put_file(token,key,local_file)
		assert ret['key']==key
		assert ret['hash']==etag(local_file)
	def __gen_download_url(self,bucket_domain,key,expire=3600):
		assert isinstance(bucket_domain,str)
		assert isinstance(key,str)
		assert isinstance(expire,int)
		base_url='http://%s/%s'%(bucket_domain,key)
		private_url=self.__auth.private_download_url(base_url,expires=expire)
		return private_url
	def download_url(self,bucket_domain,key,expire=3600):
		return self.__gen_download_url(bucket_domain,key,expire)
	def move(self,src_bucket,src_key,dest_bucket,dest_key):
		ret,info=self.__bucket.move(src_bucket,src_key,dest_bucket,dest_key)
		if ret!={}:
			return False
		return True
	def copy(self,src_bucket,src_key,dest_bucket,dest_key):
		ret,info=self.__bucket.copy(src_bucket,src_key,dest_bucket,dest_key)
		if ret !={}:
			return False
		return True
	def delete(self,bucket,key):
		ret,info=self.__bucket.delete(bucket,key)
		if ret!={}:
			return False
		return True
	def __cache_file_info(self,bucket,key,content):
		self.__file_info_cache[bucket+':'+key]=content
	def __get_file_info_from_cache(self,bucket,key,item=None):
		if item:
			return self.__file_info_cache[bucket+':'+key].get(item)
		else:
			return self.__file_info_cache[bucket+':'+key]
	def __check_file_info_cache(self,bucket,key):
		if bucket+':'+key in self.__file_info_cache:
			return True
		return False
	def file_info(self,bucket,key):
		if self.__check_file_info_cache(bucket,key):
			return self.__get_file_info_from_cache(bucket,key)
		ret,info=self.__bucket.stat(bucket,key)
		if ret:
			self.__cache_file_info(bucket,key,ret)
			return ret
		return None
	def file_size(self,bucket,key):
		if self.__check_file_info_cache(bucket,key):
			return self.__get_file_info_from_cache(bucket,key,'fsize')
		ret,info=self.__bucket.stat(bucket,key)
		if ret:
			self.__cache_file_info(bucket,key,ret)
			return ret.get('fsize')
		return None
	def file_hash(self,bucket,key):
		if self.__check_file_info_cache(bucket,key):
			return self.__get_file_info_from_cache(bucket,key,'hash')
		ret,info=self.__bucket.stat(bucket,key)
		if ret:
			self.__cache_file_info(bucket,key,ret)
			return ret.get("hash")
		return None
	def file_mime(self,bucket,key):
		if self.__check_file_info_cache(bucket,key):
			return self.__get_file_info_from_cache(bucket,key,'mimeType')
		ret,info=self.__bucket.stat(bucket,key)
		if ret:
			self.__cache_file_info(bucket,key,ret)
			return ret.get("mimeType")
		return None
	def file_create_time(self,bucket,key):
		if self.__check_file_info_cache(bucket,key):
			return self.__get_file_info_from_cache(bucket,key,'putTime')
		ret,info=self.__bucket.stat(bucket,key)
		if ret:
			self.__cache_file_info(bucket,key,ret)
			return ret.get("putTime")/1000000
		return None	

if __name__=='__main__':
	r'''
	qn=QiniuFileSystemAdapter(Config.filesystem.access_key,Config.filesystem.secret_key)
	print(qn.file_info("static-pyblog-com","image/java.jpg"))
	print(qn.file_size("static-pyblog-com","image/java.jpg"))
	print(qn.file_mime("static-pyblog-com","image/java.jpg"))
	print(qn.file_create_time("static-pyblog-com","image/java.jpg"))
	print(qn.file_hash("static-pyblog-com","image/java.jpg"))
	print(qn.upload_token("static-pyblog-com","shabi"))
	print(qn.download_url("7xs7oc.com1.z0.glb.clouddn.com","image/git.png"))
	'''
