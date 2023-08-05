#!/usr/bin/env python
#-*- coding:utf-8 -*-

#############################################
# File Name: hwpy
# Author: Stars Liao
# Mail: starsliaop@163.com
# Created Time:  2018-12-24 19:17:34
#############################################

from setuptools import setup, find_packages
with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name = "hwpy",
    version = "0.2.0",
    keywords = ("pip", "hwpy","Hardware"),
    description = "Show Linux Hardware Info",
    long_description = long_description,
    long_description_content_type="text/markdown",
    license = "MIT Licence",

    url = "https://github.com/starsliao/hwpy",
    author = "Stars Liao",
    author_email = "starsliao@163.com",

    packages = find_packages(),
    include_package_data = True,
    platforms = "any",
    install_requires = ["psutil==5.4.8"],
    classifiers=[
        'Intended Audience :: System Administrators',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Topic :: Utilities',
        ],
)
