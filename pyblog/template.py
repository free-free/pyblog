#!/usr/bin/env python3.5
# -*- coding:utf-8 -*-
import os
from pyblog.config import Config
try:
    from jinja2 import Environment, FileSystemLoader
except ImportError:
    raise ImportError("Can't import jinja2 module")


class Jinja2Template(Environment):

    def __init__(self, path, **kw):
        options = {}
        assert isinstance(kw.get("autoescape", True), bool)
        assert isinstance(kw.get("block_start_string", "{%"), str)
        assert isinstance(kw.get("block_end_string", "%}"), str)
        assert isinstance(kw.get("variable_start_string", "{{"), str)
        assert isinstance(kw.get("variable_end_string", "}}"), str)
        assert isinstance(kw.get("auto_reload", True), bool)
        assert isinstance(path, str)
        options = dict(
            autoescape=kw.get("autoescape", True),
            block_start_string=kw.get("block_start_string", '{%'),
            block_end_string=kw.get("block_end_string", "%}"),
            variable_start_string=kw.get("variable_start_string", "{{"),
            variable_end_string=kw.get("variable_end_string", "}}"),
            auto_reload=kw.get("auto_reload", True)
        )
        self._options = options
        super(Jinja2Template, self).__init__(
            loader=FileSystemLoader(path), **self._options)

    def render(self, template, **kw):
        assert isinstance(template, str)
        return self.get_template(template).render(**kw)


class Template(object):
    _template_drivers = {"jinja2": Jinja2Template}

    def __init__(self, template_driver="jinja2", template_path=Config.app.template_path, **kw):
        assert isinstance(template_driver, str)
        assert isinstance(template_path, str)
        assert template_driver in self._template_drivers, "not support template %s" % template_driver
        if template_path.find('.') == 0:
            template_path = os.path.join(os.path.dirname(
                os.path.dirname(__file__)), template_path)
        self._template_driver_instance = self._template_drivers[
            template_driver](template_path, **kw)

    def render(self, template, **kw):
        return self._template_driver_instance.render(template, **kw)
