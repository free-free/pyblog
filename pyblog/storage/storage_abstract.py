#-*- coding:utf-8 -*-
import logging
logging.basicConfig(level=logging.ERROR)


class StorageAbstractAdapter:
    r"""
            A abatract interface class ,that provides a common interface to access it for different third party service

    """

    def __init__(self, *args, **kw):
        r"""
                The init parameter is unique for different storage service
        """
        pass

    def move(self, src, dest):
        r"""
            @move a file 
            @parameters:
                src:source file name,must be 'str' type
                dest:destination file name,must be 'str' type
        """
        raise NotImplementedError

    def copy(self, src, dest):
        r"""
            @copy a file
            @parameters:
                src:source file name,'str' type
                dest:destination file name,'str' type
        """
        raise NotImplementedError

    def delete(self, src):
        r"""
            @delete a file 
        """
        raise NotImplementedError

    def file_size(self, file_name):
        r"""
            @get file size information
        """
        raise NotImplementedError

    def file_hash(self, file_name):
        r"""
            @get file hash value
        """
        raise NotImplementedError

    def file_info(self, file_name):
        r"""
            @get file all information
        """
        raise NotImplementedError

    def file_mime(self, file_name):
        r"""
            @get file mime type information
        """
        raise NotImplementedError

    def file_create_time(self, file_name):
        r"""
            @get file create time
        """
        raise NotImplementedError

    def put(self, token, file_name, **kw):
        r'''
            @update a file
        '''
        raise NotImplementedError

    def token(self, file_name, **kw):
        r"""
            @generate upload token 
        """
        raise NotImplementedError

    def get(self, file_name, **kw):
        r"""
            @download file 
        """
        raise NotImplementedError

    def get_url(self, file_name, **kw):
        r"""
            @generate download file url
        """
        raise NotImplementedError
