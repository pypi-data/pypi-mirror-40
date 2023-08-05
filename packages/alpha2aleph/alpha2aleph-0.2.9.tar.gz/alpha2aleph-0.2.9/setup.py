#!/usr/bin/env python3
# -*- coding: utf-8 -*-
################################################################################
#    alpha2aleph Copyright (C) 2018 Suizokukan
#    Contact: suizokukan _A.T._ orange dot fr
#
#    This file is part of alpha2aleph.
#    alpha2aleph is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    alpha2aleph is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with alpha2aleph.  If not, see <http://www.gnu.org/licenses/>.
################################################################################
"""
        alpha2aleph by suizokukan (suizokukan AT orange DOT fr)
        ________________________________________________________________________

        setup.py is a file required by Pypi.
        ________________________________________________________________________

        see README.md for more documentation.
"""
# Pylint : disabling the "Using the global statement (global-statement)" warning
# pylint: disable=W0622

from codecs import open
from os import path
from setuptools import setup, find_packages

from alpha2aleph.glob import __projectname__, __version__, __author__, __email__, \
                             __license__, __licensepypi__, \
                             __statuspypi__

HERE = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(HERE, 'README.rst'), encoding='utf-8') as f:
    LONG_DESCRIPTION = f.read()

setup(
    name=__projectname__,

    # The project's main homepage.
    url='https://github.com/suizokukan/alpha2aleph',

    # Versions should comply with PEP440.  For a discussion on single-sourcing
    # the version across setup.py and the project code, see
    # https://packaging.python.org/en/latest/single_source_version.html
    version=__version__,

    description="GPLv3/Python3/CLI script to convert something like 'mlḵ' in 'כלמ'",
    long_description=LONG_DESCRIPTION,

    # Author details
    author=__author__,
    author_email=__email__,

    # Choose your license
    license=__license__,

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        __statuspypi__,

        # Indicate who your project is intended for
        'Intended Audience :: Education',
        'Topic :: Utilities',

        # Pick your license as you wish (should match "license" above)
        __licensepypi__,

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 3',
    ],

    # What does your project relate to?
    keywords='text hebrew translitteration',

    # You can just specify the packages manually here if your project is
    # simple. Or you can use find_packages().
    #
    # !!! I got problems with find_packages(), unable to detect the directories
    # !!!  with code, maybe since I don't add __init__.py file anymore.
    #
    packages=['alpha2aleph',],

    install_requires=[],

    include_package_data = False,

    # To provide executable scripts, use entry points in preference to the
    # "scripts" keyword. Entry points provide cross-platform support and allow
    # pip to create the appropriate form of executable for the target platform.
    entry_points={
        'console_scripts': ['alpha2aleph=alpha2aleph.main:entrypoint',],
    },
)
