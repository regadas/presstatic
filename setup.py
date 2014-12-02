#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import presstatic
from pip.req import parse_requirements

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


install_reqs = parse_requirements('requirements.txt')
install_requires = [str(ir.req) for ir in install_reqs]


def publish():
    """Publish to PyPi"""
    os.system("python setup.py sdist upload")


if sys.argv[-1] == "publish":
    publish()
    sys.exit()


setup(
    name='presstatic',
    version=presstatic.__version__,
    description='Deploy static websites to Amazon S3 easily.',
    long_description=open('README.rst').read(),
    author='Filipe Regadas',
    author_email='filipe@regadas.org',
    url='https://github.com/regadas/presstatic',
    data_files=[
        'README.rst'
    ],
    packages=[
        'presstatic',
        'presstatic.storage',
    ],
     entry_points={
        'console_scripts': [
            'pstatic = presstatic.__main__:main',
            'presstatic = presstatic.manage:main',
        ],
    },
    install_requires=install_requires,
    license='MIT',
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
        'License :: OSI Approved :: MIT License',
        'Topic :: Internet',
        'Topic :: Terminals',
        'Topic :: Utilities'
    ),
)
