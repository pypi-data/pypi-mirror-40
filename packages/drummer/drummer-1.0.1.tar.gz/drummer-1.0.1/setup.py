#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from setuptools import setup

with open('README.md','r') as f:
    long_description = f.read()

setup(
    name='drummer',
    version='1.0.1',
    description='Multi-process, multi-tasking scheduler',
    author='andrea capitanelli',
    author_email='andrea.capitanelli@gmail.com',
    maintainer='andrea capitanelli',
    maintainer_email='andrea.capitanelli@gmail.com',
    url='https://github.com/drummer',
    packages=[
        'drummer'
    ],
    install_requires=[
        'blessings',
        'croniter',
        'inquirer',
        'PTable',
        'PyYAML',
        'readchar',
        'six',
        'SQLAlchemy',
    ],
    long_description=long_description,
    keywords='scheduler extender multi-process multi-tasking',
    license='MIT',
    classifiers=[
      'Development Status :: 3 - Alpha',
      'License :: OSI Approved :: MIT License',
      'Programming Language :: Python :: 3',
      'Topic :: System'
    ],
    scripts=[
        'bin/drummer-admin'
    ],
)
