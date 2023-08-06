# -*- coding: utf-8 -*-

from setuptools import setup


with open('README.md') as f:
    readme = f.read()

setup(
    name='wanwei-test',
    version='0.0.1',
    description='health checker for MySQL database',
    long_description=readme,
    author='Wanwei',
    author_email='784971886@qq.com',
    url='https://github.com/wanwei890116/test',
    packages=['test1']
)

