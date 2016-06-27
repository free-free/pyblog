#-*- coding:utf-8 -*-

from pyblog.config import Config
from pyblog.storage.storage_factory import StorageDriverFactory


class Storage(object):

    def __init__(self, disk=None, config=None):
        if disk and not config:
            self.__disk = disk
            self.__config = Config.storage.disk(self.__disk).all
        elif disk and config:
            self.__disk = disk
            self.__config = Config.storage.disk(self.__disk).all
            self.__config = config
        else:
            self.__disk = Config.storage.disk_name
            self.__config = Config.storage.all
        self.__resovled_storage_instance = {}
        self.__current_disk = self._disk(
            self.__config.get('driver'), self.__config)
        self.__resovled_storage_instance[self.__disk] = self
        self.__factory = StorageDriverFactory

    def _disk(self, driver, config):
        return self.__factory(driver, config)

    def disk(self, disk_name, config=None):
        if disk_name not in self.__resolved_storage_instance:
            self.__resolved_storage_instance[
                disk_name] = Storage(disk_name, config)
        return self.__resolved_storage_instance[disk_name]

    def move(self, src, dest):
        return self.__current_disk.move(src, dest)

    def rename(self, src_old, src_new):
        return self.move(src_old, src_new)

    def copy(self, src, dest):
        return self.__current_disk.copy(src, dest)

    def delete(self, file_name):
        return self.__current_disk.delete(file_name)

    def file_size(self, file_name):
        return self.__current_disk.file_size(file_name)

    def file_hash(self, file_name):
        return self.__current__disk.file_hash(file_name)

    def file_ctime(self, file_name):
        return self.__current_disk.file_create_time(file_name)

    def file_mime(self, file_name):
        return self.__current_disk.file_mime(file_name)

    def token(self, file_name, **kw):
        return self.__current_disk.token(file_name, **kw)

    def put(self, file_name, local_file, **kw):
        return self.__current_disk.put(file_name, local_file, **kw)

    def get(self, file_name, **kw):
        pass

    def get_url(self, file_name, **kw):
        return self.__current_disk.get_url(file_name, **kw)
if __name__ == '__main__':
    pass
