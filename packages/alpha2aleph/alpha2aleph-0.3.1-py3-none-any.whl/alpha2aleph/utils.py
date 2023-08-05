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

        utils.py : various usefull functions
"""
import re
import os
import os.path
import unicodedata


def stranalyse(src):
    """
       stranalyse()
       ________________________________________________________________________

       Analyse the string <src> and return a lot of informations about each
       character.
       ________________________________________________________________________

       PARAMETER      : (str)src, the source string.

       RETURNED VALUE : (str)the result of <src>.
    """
    res = []
    for char in src:
        name = unicodedata.name(char)
        res.append('\"{0}\"(#{1})={2}'.format(char,
                                              hex(ord(char)),
                                              name))
    return ";".join(res)


def match_repr(match):
    """
       match_repr()
       ________________________________________________________________________

       Return a human readable representation of <match>
       ________________________________________________________________________

       PARAMETER      : (_sre.SRE_Match)the source match object.

       RETURNED VALUE : (str)a human readable representation of <match>
    """
    return "(indexes {0} to {1}) : '{2}'".format(match.start(), match.end(), match.group())


def extract_around_index(string, index, amplitude=10):
    """
       extract_around_index()
       ________________________________________________________________________

       Return the extract centered around string[index] +/- amplitude.
       ________________________________________________________________________

       PARAMETER      : (str)string, the source string
                        (int)index, index in string
                        (int)amplitude

       RETURNED VALUE : (str)the expected extract around string[index]
    """
    index0 = max(0, index-amplitude)
    index1 = min(len(string)-1, index+amplitude)

    before = "…"
    if index0 == 0:
        before = ""

    after = "…"
    if index1 == len(string)-1:
        after = ""

    return before+string[index0:index1]+after


def extracts(target, src, amplitude=10):
    """
       extracts()
       ________________________________________________________________________

       Return all occurences of <target> in <src> using +/- <amplitude>.
       ________________________________________________________________________

       PARAMETER      : (str)target, the string to be find in <target>
                        (str)src, the source string
                        (int)amplitude

       RETURNED VALUE : (str)the resulting string
    """
    res = []

    for _res in re.finditer(target, src):
        index0 = _res.start()
        _index0 = max(0, index0 - amplitude)

        index1 = _res.end()
        _index1 = min(len(src)-1, index1 + amplitude)

        res.append("…" + src[_index0:index0] + _res.group() + src[index1:_index1] + "…")

    finalres = []
    for i, _res in enumerate(res):
        finalres.append("(#{0}) : \"{1}\"".format(i, _res))

    res = " /// ".join(finalres)
    if res:
        return res
    return "(empty extract)"


def normpath(path):
    """
        normpath()
        ________________________________________________________________________

        Return a human-readable (e.g. "~" -> "/home/myhome/" on Linux systems),
        normalized version of a path.

        The returned string may be used as a parameter given to by
        os.path.exists() .
        ________________________________________________________________________

        PARAMETER : (str)path

        RETURNED VALUE : the expected string
    """
    res = os.path.normpath(os.path.abspath(os.path.expanduser(path)))

    if res == ".":
        res = os.getcwd()

    return res
