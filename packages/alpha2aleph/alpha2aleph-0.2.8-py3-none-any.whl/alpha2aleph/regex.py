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

        regex.py : regex utilities
"""
import re
import alpha2aleph.globalsrtl

LOGGER = alpha2aleph.glob.LOGGER


def get_rtlreader_regex():
    """
       get_rtlreader_regex()
       ________________________________________________________________________

       Return a regex allowing to extract text between RTL markers, markers
       defined by alpha2aleph.globalsrtl.RTL_SYMBOLS .
       ________________________________________________________________________

       no PARAMETER

       RETURNED VALUE : the compiled regex
    """
    rtl_start, rtl_end = alpha2aleph.globalsrtl.RTL_SYMBOLS

    if rtl_start == rtl_end:
        res = '{0}(?P<rtltext>[^{0}]*){0}'.format(re.escape(rtl_start))
    else:
        res = '{0}(?P<rtltext>[^{0}{1}]*){1}'.format(re.escape(rtl_start),
                                                     re.escape(rtl_end))

    alpha2aleph.glob.LOGGER.debug("[D01] new RTLREADER_REGEX : %s", res)

    return re.compile(res)
