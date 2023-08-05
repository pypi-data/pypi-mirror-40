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

        A (Python3/GPLv3/Linux/CLI) project, using no additional
        modules than the ones installed with Python3.

        alphabetic text → translitteration → Hebrew text

        see README.md for more documentation.
        ________________________________________________________________________

        glob.py : global declarations
"""
import logging

__projectname__ = "alpha2aleph"
__version__ = "0.2.9"
__license__ = "GPLv3"
__author__ = "Xavier Faure (suizokukan / 94.23.197.37)"
__email__ = "suizokukan@orange.fr"
__copyright__ = "Copyright 2018, suizokukan"
__license__ = "GPL-3.0"
__licensepypi__ = 'License :: OSI Approved :: GNU General Public License v3 (GPLv3)'
__maintainer__ = "Xavier Faure (suizokukan)"
__status__ = "Pre-Alpha"
__statuspypi__ = 'Development Status :: 2 - Pre-Alpha'
__location__ = "github.com/suizokukan/alpha2aleph"

LOGGER = None
LOGGING_LEVEL = logging.INFO

ALPHA2HEBREW = None
ALPHA2HEBREW_KEYS = None
