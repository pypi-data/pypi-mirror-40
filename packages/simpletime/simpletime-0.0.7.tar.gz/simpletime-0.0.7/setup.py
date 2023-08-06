#!/usr/bin/env python
# coding: utf-8

from setuptools import setup
# from distutils.core import setup

"""
发布simpletime模块
"""

#__version__ = '0.0.1'
#__author__  = 'Area0 Li <area0cn@gmail.com>'

with open('manual') as file:
	manual = file.read()

setup(
    name              = 'simpletime',
    version           = '0.0.7',
    author            = 'Area0 Li <area0cn@gmail.com>',
    author_email      = 'area0cn@gmail.com',
    license           = 'Mozilla Public License 2.0',
    description       = ('simple to date and time conver'),
    #platforms        = '',
    url               = 'https://github.com/area0li/simpletime',
    #packages         =['simpletime'],
    py_modules        = ['simpletime'],
    long_description  = manual,
    long_description_content_type="text/markdown",
)
