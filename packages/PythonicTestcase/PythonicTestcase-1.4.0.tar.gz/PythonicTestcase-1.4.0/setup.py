#!/usr/bin/env python3
#
# SPDX-License-Identifier: MIT

import os

from setuptools import setup

def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

setup(
    name = 'PythonicTestcase',
    version = '1.4.0',
    description = 'standalone pythonic assertions',
    long_description=(read('Changelog.txt')),

    author='Felix Schwarz',
    author_email='felix.schwarz@oss.schwarz.eu',
    license='MIT',
    url='https://bitbucket.org/felixschwarz/pythonic-testcase/',

    py_modules=['pythonic_testcase'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],

)
