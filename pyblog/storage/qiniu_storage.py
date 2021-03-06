#-*- coding:utf-8 -*-
import logging
logging.basicConfig(level=logging.ERROR)
from pyblog.config import Config
from pyblog.storage.storage_abstract import StorageAbstractAdapter
try:
    from qiniu import Auth, put_file, etag, urlsafe_base64_encode, BucketManager
    import qiniu.config
except ImportError:
    logging.error("can't import 'qiniu' module")
    exit(-1)


class QiniuStorageAdapter(StorageAbstractAdapter):
    __slots__ = ('__access_key', '__secret_key', '__auth', '__bucket',
                 '__file_info_cache', '__bucket_manager', '__domain')

    def __init__(self, config, *args, **kw):
        assert isinstance(config, dict)
        assert isinstance(config.get("bucket"), str)
        assert isinstance(config.get("access_key"), str)
        assert isinstance(config.get("secret_key"), str)
        assert isinstance(config.get("domain"), str)
        self.__access_key = config.get("access_key")
        self.__secret_key = config.get("secret_key")
        self.__bucket = config.get("bucket")
        self.__domain = config.get("domain")
        self.__auth = Auth(self.__access_key, self.__secret_key)
        self.__bucket_manager = BucketManager(self.__auth)
        self.__file_info_cache = {}

    def __gen_upload_token(self, file_name, expire=3600, policy=None):
        assert isinstance(file_name, str)
        assert isinstance(expire, int)
        assert isinstance(policy, (str, dict, type(None)))
        if policy:
            token = self.__auth.upload_token(
                self.__bucket, file_name, expire, policy)
        else:
            token = self.__auth.upload_token(self.__bucket, file_name, expire)
        return token

    def token(self, file_name, **kw):
        expire = kw.get("expire", 3600)
        policy = kw.get("policy")
        return self.__gen_upload_token(file_name, expire, policy)

    def put(self, file_name, local_file, **kw):
        token = kw.get('token')
        assert token, "token can't be empty"
        ret, info = put_file(token, file_name, local_file)
        assert ret['key'] == file_name
        assert ret['hash'] == etag(local_file)

    def __gen_download_url(self, bucket_domain, file_name, expire=3600):
        assert isinstance(bucket_domain, str)
        assert isinstance(file_name, str)
        assert isinstance(expire, int)
        base_url = 'http://%s/%s' % (bucket_domain, file_name)
        private_url = self.__auth.private_download_url(
            base_url, expires=expire)
        return private_url

    def get(self, file_name, **kw):
        pass

    def get_url(self, file_name, **kw):
        bucket_domain = self.__domain
        expire = kw.get("expire", 3600)
        return self.__gen_download_url(bucket_domain, file_name, expire)

    def move(self, src, dest):
        src_bucket, src_key = src.split("<:>")
        dest_bucket, dest_key = dest.split("<:>")
        ret, info = self.__bucket_manager.move(
            src_bucket, src_key, dest_bucket, dest_key)
        if ret != {}:
            return False
        return True

    def copy(self, src, dest):
        src_bucket, src_key = src.split("<:>")
        dest_bucket, dest_key = dest.split("<:>")
        ret, info = self.__bucket_manager.copy(
            src_bucket, src_key, dest_bucket, dest_key)
        if ret != {}:
            return False
        return True

    def delete(self, file_name):
        ret, info = self.__bucket_manager.delete(self.__bucket, file_name)
        if ret != {}:
            return False
        return True

    def __cache_file_info(self, file_name, content):
        self.__file_info_cache[self.__bucket + ':' + file_name] = content

    def __get_file_info_from_cache(self, file_name, item=None):
        if item:
            return self.__file_info_cache[self.__bucket + ':' + file_name].get(item)
        else:
            return self.__file_info_cache[self.__bucket + ':' + file_name]

    def __check_file_info_cache(self, file_name):
        if self.__bucket + ':' + file_name in self.__file_info_cache:
            return True
        return False

    def __get_file_info_item(self, file_name, item):
        if self.__check_file_info_cache(file_name):
            return self.__get_file_info_from_cache(file_name, item)
        ret, info = self.__bucket_manager.stat(self.__bucket, file_name)
        if ret:
            self.__cache_file_info(file_name, ret)
            return self.__get_file_info_from_cache(file_name, item)
        return None

    def file_info(self, file_name):
        return self.__get_file_info_item(file_name, None)

    def file_size(self, file_name):
        return self.__get_file_info_item(file_name, 'fsize')

    def file_hash(self, file_name):
        return self.__get_file_info_item(file_name, 'hash')

    def file_mime(self, file_name):
        return self.__get_file_info_item(file_name, 'mimeType')

    def file_create_time(self, file_name):
        return self.__get_file_info_item(file_name, 'putTime')

if __name__ == '__main__':
    pass
