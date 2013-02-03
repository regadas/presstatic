#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

import presstatic


def publish():
    """Publish to PyPi"""
    os.system("python setup.py sdist upload")

if sys.argv[-1] == "publish":
    publish()
    sys.exit()

required = [
    'clint>=0.3.1',
    'simplejson>=3.0.7',
    'boto>=2.8.0',
]

setup(
    name='presstatic',
    version=presstatic.__version__,
    description='Python Command-line Application Tools',
    long_description=open('README.rst').read(),
    author='Filipe Regadas',
    author_email='filipe@regadas.org',
    url='https://github.com/regadas/presstatic',
    data_files=[
        'README.rst'
    ],
    packages=[
        'presstatic',
    ],
     entry_points={
        'console_scripts': [
            'pstatic = presstatic.__main__:main',
            'presstatic = presstatic.manage:main',
        ],
    },
    install_requires=required,
    license='BSD',
    classifiers=(
#       'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.1',
        'Programming Language :: Python :: 3.2',
        'License :: OSI Approved :: BSD License',
        'Topic :: Internet',
        'Topic :: Terminals',
        'Topic :: Utilities'
    ),
)
