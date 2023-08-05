#!/usr/bin/env python
#-*- coding:utf-8 -*-

#############################################
# File Name: hwinfo
# Author: Stars Liao
# Mail: starsliaop@163.com
# Created Time:  2018-12-24 19:17:34
#############################################

from setuptools import setup, find_packages

setup(
    name = "hwpy",
    version = "0.1.0",
    keywords = ("pip", "hwinfo","Hardware"),
    description = "hwpy",
    long_description = "Show Linux Hardware Info",
    license = "MIT Licence",

    url = "https://github.com/starsliao/hwpy",
    author = "Stars Liao",
    author_email = "starsliao@163.com",

    packages = find_packages(),
    include_package_data = True,
    platforms = "any",
    install_requires = ["psutil"],
    classifiers=[
        'Intended Audience :: System Administrators',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Topic :: Utilities',
        ],
)
