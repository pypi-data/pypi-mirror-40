# -*- encoding:utf8 -*-
#================================================================
#   Copyright (C) 2018 Seetatech. All rights reserved.
#   
#   文件名称：setup.py
#   创 建 者： seetatech & xuboxuan
#   创建日期：2018年07月09日
#   描    述：
#
#================================================================

try:
    from setuptools import setup, find_packages, Extension
except ImportError:
    from distutils.core import setup, find_packages
import sys,os

setup(
    name='seetaas-helper',
    version='1.6',
    author='SeetaTech',
    author_email='boxuan.xu@seetatech.com',
    license='MIT',
    platforms='any',
    packages=find_packages(),
    install_requires=[
        'requests==2.18.4',
        'gunicorn',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Operating System :: OS Independent',
    ],
)

