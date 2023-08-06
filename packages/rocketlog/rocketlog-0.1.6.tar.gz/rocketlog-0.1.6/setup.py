#!/usr/bin/env python
from __future__ import print_function
from setuptools import setup, find_packages
import sys
 
setup(
    name='rocketlog',
    version="0.1.6",
    author="grayzhang",
    author_email="plyj0123@163.com",
    description="add bin file",
    license="MIT",
    packages=find_packages(),
    install_requires = ['rocket-python'],
    url="https://github.com/graylzhang/rocketlog"
)

