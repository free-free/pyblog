# -*- coding:utf-8 -*-


import os
import time
import asyncio
import json
import logging
logging.basicConfig(level=logging.ERROR)
from aiohttp import web
from pyblog.log import Log
from pyblog.httptools import Middleware, Route
from pyblog.template import Template
from pyblog.config import Config
from pyblog.database import DB
from pyblog.session import SessionManager
logging.basicConfig(level=logging.INFO)


__all__ = ("Application",)


class Application(web.Application):

    def __init__(self):
        self._loop = asyncio.get_event_loop()
        super(Application, self).__init__(loop=self._loop,
                                          middlewares=Middleware.allmiddlewares())

    def run(self, addr='127.0.0.1', port='8000'):
        self._server = self._loop.run_until_complete(
            self.get_server(addr, port))
        try:
            self._loop.run_forever()
        except KeyboardInterrupt:
            pass
        finally:
            self._db_pool.close()
            self._loop.run_until_complete(self._db_pool.wait_closed())
            self._server.close()
            self._loop.run_until_complete(self._server.wait_closed())
            self._loop.run_until_complete(self.shutdown())
            self._loop.run_until_complete(self._handler.finish_connections(60))
            self._loop.run_until_complete(self.cleanup())
        self._loop.close()

    @asyncio.coroutine
    def get_server(self, addr, port):
        self['__templating__'] = Template()
        Route.register_route(self)
        self._db_pool = yield from DB.createpool(self._loop)
        self._handler = self.make_handler()
        server = yield from self._loop.create_server(self._handler, addr, port)
        Log.info("server start at http://%s:%s" % (addr, port))
        print("server start at http://%s:%s" % (addr, port))
        return server


class AppAbstractRegister(object):
    r'''
                    AppAbstractRegister is a place where you can register your own's things that you need to use in your app procession,
                    those things mostly likes your task queue executor and so on
    '''

    def __init__(self, *args, **kwargs):
        pass

    def process(self):
        r"""
                logic code ,you want to use register
        """
        pass


class _Application(dict):

    def __init__(self, request, *args, **kw):
        super(_Application, self).__init__(**kw)
        self.__request = request

    def get_cookie(self, name, default=None):
        return self.__request.cookies.get(name, default)

    def get_all_cookies(self):
        return self.__request.cookies

    def set_cookies(self, name, val, expires=None, domain=None, max_age=None, httponly=False, path='/'):
        pass

    def get_argument(self, name, default=None):
        pass

    def get_arguments(self, name, default=None):
        pass

    def set_status(self, status_code, reason):
        pass

    def render(self, template, **kw):
        pass

    def add_header(self, header_name, header_content):
        pass

    def get_header(self, header_name):
        pass
