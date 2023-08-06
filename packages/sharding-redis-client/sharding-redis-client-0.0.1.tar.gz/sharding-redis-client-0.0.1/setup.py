#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(name='sharding-redis-client',
      version='0.0.1',
      description=(
          'python shared redis client'
      ),
      long_description=open('README.text').read(),
      author='hanshuo',
      author_email='837145493@qq.com',
      maintainer='hanshuo',
      maintainer_email='837145493@qq.com',
      license='BSD License',
      packages=['src'],
      platforms=["all"],
      url='https://github.com/gantang001/deep-minding.',
      classifiers=[
          'Development Status :: 4 - Beta',
          'Operating System :: OS Independent',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: BSD License',
          'Programming Language :: Python',
          'Programming Language :: Python :: Implementation',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 2.7',
          'Topic :: Software Development :: Libraries'
      ],
      install_requires=[
          'redis>=2.10.6'
      ]
      )
