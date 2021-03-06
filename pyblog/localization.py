#-*- coding:utf-8 -*-
import os
import json
import re
import time
from pyblog.config import Config


class LocaleProxyer(dict):
    _locale_file_dir = None
    _locale_files_content = {}

    def __init__(self, locale_file_dir):
        assert isinstance(locale_file_dir, str)
        if type(self)._locale_file_dir != os.path.abspath(locale_file_dir):
            type(self)._locale_file_dir = os.path.abspath(locale_file_dir)

    def get_locale_item(self, filename, item):
        items = item.split('.')
        absfilename = os.path.join(self._locale_file_dir, filename)
        if absfilename not in self:
            if os.path.exists(absfilename):
                with open(absfilename) as f:
                    self[absfilename] = json.load(f)
        item_content = self[absfilename]
        for item_name in items:
            try:
                tmp_content = item_content[item_name]
            except Exception:
                item_content = None
            else:
                item_content = tmp_content
        return item_content


class Locale(object):
    _locale_dir = os.path.abspath(os.path.join(
        os.path.dirname(os.path.dirname(__file__)), 'locale'))
    _locale_file_suffix = '.py'

    def __init__(self, locale_proxyer=LocaleProxyer):
        self._locale_proxyer = locale_proxyer(
            os.path.join(self._locale_dir, Config.app.locale))

    def translate(self, key, **kw):
        self._parameters = kw or {}
        item_content = self._locale_proxyer.get_locale_item(
            self._parse_locale_filename(key), self._parse_locale_items(key))
        if not item_content:
            if 'default' in self._parameters:
                return self._parameters.get('default')
        else:
            item_content = self._translate(item_content)
        return item_content

    def _translate(self, items):
        if isinstance(items, str):
            return self._str_translate(items)
        elif isinstance(items, dict):
            translated_items = {}
            for key, item_content in items.items():
                translated_items[key] = self._translate(item_content)
            return translated_items
        elif isinstance(items, list):
            translated_items = []
            for item_content in items:
                translated_items.append(self._translate(item_content))
            return translated_items
        else:
            return items

    def _dict_translate(self, items):
        translated_items = {}
        for key, item_content in items:
            translated_items[key] = self._str_translate(item_content)
        return translated_items

    def _list_translate(self, items):
        translated_items = []
        for item_content in items:
            translated_items.append(self._str_translate(item_content))
        return translated_items

    def _str_translate(self, item_content):
        return self._fill_parameter(item_content)

    def _fill_parameter(self, content):
        return re.sub(r'{\s*[\w]+\s*}', self._replace_parameter, content)

    def _replace_parameter(self, matched):
        matched = matched.group(0)[1:-1].strip()
        if matched in self._parameters:
            return str(self._parameters.get(matched, ''))
        return ''

    def _parse_locale_filename(self, key):
        return key.split(':')[0] + self._locale_file_suffix

    def _parse_locale_items(self, key):
        return key.split(':')[1]

if __name__ == '__main__':
    r'''
    #l=Locale()
    #print(l.translate('message:register'))
    #l._fill_parameter("{  name  }d fsfesfe{  age  }")
    #print(l.translate('message:register',default='password wrong',username="whoami",email="19941222hb@gmail.com",time=time.time()))
    #print(l.translate('message:login.password'))
    #print(LocaleProxyer('../locale/chinese').get_locale_item('message.py','login.email'))
    '''
