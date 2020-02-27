# -*- coding: utf-8 -*-
# 15/6/10
# create by: snower

import os
from setuptools import find_packages, setup

version = "0.0.1"

if os.path.exists("README.md"):
    with open("README.md") as fp:
        long_description = fp.read()
else:
    long_description = ''

setup(
    name='mgtail',
    version=version,
    url='https://github.com/snower/mgtail',
    author='snower',
    author_email='sujian199@gmail.com',
    license='MIT',
    packages=find_packages(),
    zip_safe=False,
    install_requires=[
        'tornado>=6.0.3',
        'thrift==0.13.0',
        'torthrift>=0.2.3',
        'motor>=2.1.0',
        'greenlet>=0.4.2',
    ],
    package_data={
        '': ['README.md'],
    },
    entry_points={
        'console_scripts': [
            'mgtail = forsun.scripts.mgtail:main',
            'mgtaild = forsun.scripts.mgtaild:main',
        ],
    },
    description= 'mongodb capped tail',
    long_description= long_description,
)
