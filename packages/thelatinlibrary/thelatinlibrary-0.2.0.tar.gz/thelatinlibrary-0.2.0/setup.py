#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is a part of thelatinlibrary
#
# Copyright (c) 2018 The thelatinlibrary Authors (see AUTHORS)
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import io
import os
from setuptools import setup

here = os.path.abspath(os.path.dirname(__file__))

try:
    with io.open(os.path.join(here, 'README.md'), encoding='utf-8') as file:
        long_description = '\n' + file.read()
except FileNotFoundError:
    long_description = 'An unofficial thelatinlibrary.com client'

setup(
    author='hearot',
    author_email='gabriel@hearot.it',
    classifiers=[
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7'
    ],
    description='An unofficial thelatinlibrary.com client',
    long_description=long_description,
    long_description_content_type='text/markdown',
    license='GNU GENERAL PUBLIC LICENSE',
    install_requires=['BeautifulSoup4', 'dataclasses', 'html5lib', 'requests'],
    name='thelatinlibrary',
    packages=['thelatinlibrary'],
    python_requires='>=3.6.0',
    url='https://github.com/hearot/thelatinlibrary',
    version='0.2.0'
)
