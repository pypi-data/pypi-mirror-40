# -*- coding: utf-8 -*-
from setuptools import setup

setup(name='nissaprinterserver',
      version='1.1',
      description='Nisssa Makbuz Printer Server',
      url='http://github.com/coderprofile/nissaprinterserver',
      author='Yasin BIKMAZER',
      author_email='yasin@nissayazilim.com',
      license='MIT',
      packages=['nissaprinterserver'],
      keywords='dotmatrix printer server',
      install_requires=[
          'flask',
      ],
      zip_safe=False)