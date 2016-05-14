#!/usr/bin/env python3.5
import os
import sys
from setuptools import find_packages,setup

setup(
	name="pyblog",
	version="1.1",
	author="whoami",
	author_email="19941222hb@gmail.com",
	description="An asynchronous web framework that base on aiohttp",
	license="MIT",
	packages=find_packages(),
	include_package_data=True,
	install_requires=[line for line in open('requirements.txt','r').read()]
)
