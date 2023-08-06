# -*- coding: utf-8 -*-
# Author: ZhangTianJie

import setuptools

with open('README.md', 'r', encoding='utf8') as fh:
    long_description = fh.read()

setuptools.setup(
    name='py_configfile',
    version='0.0.2',
    description='python configuration file loading package',
    long_description=long_description,
    long_description_content_type="text/markdown",

    py_modules=["configfile"],

    url='http://github.com/ztj1993/py_configfile',
    author='ZhangTianJie',
    author_email='ztj1993@gmail.com',

    keywords='configfile config json yaml',
    install_requires=['pyyaml'],

    license='MIT',
)
