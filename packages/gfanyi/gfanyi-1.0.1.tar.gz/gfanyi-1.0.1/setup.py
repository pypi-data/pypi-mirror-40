#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Note: To use the 'upload' functionality of this file, you must:
#   $ pip install twine

# from distutils.core import setup
from setuptools import setup, find_packages

setup(
    name='gfanyi',
    version='1.0.1',
    packages=find_packages(),
    requires=['requests','execjs','html'],
    url='https://github.com/xujinjie151/gfanyi',
    license='',
    author='xujinjie151',
    author_email='xujinjie151@gmail.com',
    description='G翻译'
)



