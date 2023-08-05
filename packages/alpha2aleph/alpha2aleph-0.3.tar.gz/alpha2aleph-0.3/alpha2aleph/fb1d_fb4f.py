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

        fb4d_fb4F : special unicode characters between 0xFB4D and 0xFB4F
"""

#
# format:
#    for shortname, (fullname, before, after) in TRANSF_FB1D_FB4F:
#        ...
#    fullname MUST BE .ini-COMPATIBLE : no upper cases, no ":"

# how read TRANSF_FB1D_FB4F ?
# for shortname, (fullname, before, after) in TRANSF_FB1D_FB4F:
#     ...
TRANSF_FB1D_FB4F = (
    ("0x05d9+0x05b4→0xfb1d", ("(0x05d9+0x05b4→0xfb1d) hebrew letter yod with hiriq",
                              chr(0x05d9) + chr(0x05b4),
                              chr(0xfb1d))),

    ("0x05f2+0x05b7→0xfb1f", ("(0x05f2+0x05b7→0xfb1f) hebrew ligature yiddish yod yod patah",
                              chr(0x05f2) + chr(0x05b7),
                              chr(0xfb1f))),

    ("0x05e9+0x05c1→0xfb2a", ("(0x05e9+0x05c1→0xfb2a) hebrew letter shin with shin dot",
                              chr(0x05e9) + chr(0x05c1),
                              chr(0xfb2a))),

    ("0x05e9+0x05c2→0xfb2b", ("(0x05e9+0x05c2→0xfb2b) hebrew letter shin with sin dot",
                              chr(0x05e9) + chr(0x05c2),
                              chr(0xfb2b))),

    ("0x05d0+0x05b7→0xfb2e", ("(0x05d0+0x05b7→0xfb2e) hebrew letter alef with patah",
                              chr(0x05d0) + chr(0x05b7),
                              chr(0xfb2e))),

    ("0x05d0+0x05b8→0xfb2f", ("(0x05d0+0x05b8→0xfb2f) hebrew letter alef with qamats",
                              chr(0x05d0) + chr(0x05b8),
                              chr(0xfb2f))),

    ("0x05d0+0x05bc→0xfb30", ("(0x05d0+0x05bc→0xfb30) hebrew letter alef with mapiq",
                              chr(0x05d0) + chr(0x05bc),
                              chr(0xfb30))),

    ("0x05d1+0x05bc→0xfb31", ("(0x05d1+0x05bc→0xfb31) hebrew letter bet with dagesh",
                              chr(0x05d1) + chr(0x05bc),
                              chr(0xfb31))),

    ("0x05d2+0x05bc→0xfb32", ("(0x05d2+0x05bc→0xfb32) hebrew letter gimel with dagesh",
                              chr(0x05d2) + chr(0x05bc),
                              chr(0xfb32))),

    ("0x05d3+0x05bc→0xfb33", ("(0x05d3+0x05bc→0xfb33) hebrew letter dalet with dagesh",
                              chr(0x05d3) + chr(0x05bc),
                              chr(0xfb33))),

    ("0x05d4+0x05bc→0xfb34", ("(0x05d4+0x05bc→0xfb34) hebrew letter he with mapiq",
                              chr(0x05d4) + chr(0x05bc),
                              chr(0xfb34))),

    ("0x05d5+0x05bc→0xfb35", ("(0x05d5+0x05bc→0xfb35) hebrew letter vav with dagesh",
                              chr(0x05d5) + chr(0x05bc),
                              chr(0xfb35))),

    ("0x05d6+0x05bc→0xfb36", ("(0x05d6+0x05bc→0xfb36) hebrew letter zayin with dagesh",
                              chr(0x05d6) + chr(0x05bc),
                              chr(0xfb36))),

    ("0x05d8+0x05bc→0xfb38", ("(0x05d8+0x05bc→0xfb38) hebrew letter tet with dagesh",
                              chr(0x05d8) + chr(0x05bc),
                              chr(0xfb38))),

    ("0x05d9+0x05bc→0xfb39", ("(0x05d9+0x05bc→0xfb39) hebrew letter yod with dagesh",
                              chr(0x05d9) + chr(0x05bc),
                              chr(0xfb39))),

    ("0x05da+0x05bc→0xfb3a", ("(0x05da+0x05bc→0xfb3a) hebrew letter final kaf with dagesh",
                              chr(0x05da) + chr(0x05bc),
                              chr(0xfb3a))),

    ("0x05db+0x05bc→0xfb3b", ("(0x05db+0x05bc→0xfb3b) hebrew letter kaf with dagesh",
                              chr(0x05db) + chr(0x05bc),
                              chr(0xfb3b))),

    ("0x05dc+0x05bc→0xfb3c", ("(0x05dc+0x05bc→0xfb3c) hebrew letter lamed with dagesh",
                              chr(0x05dc) + chr(0x05bc),
                              chr(0xfb3c))),

    ("0x05de+0x05bc→0xfb3e", ("(0x05de+0x05bc→0xfb3e) hebrew letter mem with dagesh",
                              chr(0x05de) + chr(0x05bc),
                              chr(0xfb3e))),

    ("0x05e0+0x05bc→0xfb40", ("(0x05e0+0x05bc→0xfb40) hebrew letter nun with dagesh",
                              chr(0x05e0) + chr(0x05bc),
                              chr(0xfb40))),

    ("0x05e1+0x05bc→0xfb41", ("(0x05e1+0x05bc→0xfb41) hebrew letter samekh with dagesh",
                              chr(0x05e1) + chr(0x05bc),
                              chr(0xfb41))),

    ("0x05e3+0x05bc→0xfb43", ("(0x05e3+0x05bc→0xfb43) hebrew letter final pe with dagesh",
                              chr(0x05e3) + chr(0x05bc),
                              chr(0xfb43))),

    ("0x05e4+0x05bc→0xfb44", ("(0x05e4+0x05bc→0xfb44) hebrew letter pe with dagesh",
                              chr(0x05e4) + chr(0x05bc),
                              chr(0xfb44))),

    ("0x05e6+0x05bc→0xfb46", ("(0x05e6+0x05bc→0xfb46) hebrew letter tsadi with dagesh",
                              chr(0x05e6) + chr(0x05bc),
                              chr(0xfb46))),

    ("0x05e7+0x05bc→0xfb47", ("(0x05e7+0x05bc→0xfb47) hebrew letter qof with dagesh",
                              chr(0x05e7) + chr(0x05bc),
                              chr(0xfb47))),

    ("0x05e8+0x05bc→0xfb48", ("(0x05e8+0x05bc→0xfb48) hebrew letter resh with dagesh",
                              chr(0x05e8) + chr(0x05bc),
                              chr(0xfb48))),

    ("0x05e9+0x05bc→0xfb49", ("(0x05e9+0x05bc→0xfb49) hebrew letter shin with dagesh",
                              chr(0x05e9) + chr(0x05bc),
                              chr(0xfb49))),

    ("0x05ea+0x05bc→0xfb4a", ("(0x05ea+0x05bc→0xfb4a) hebrew letter tav with dagesh",
                              chr(0x05ea) + chr(0x05bc),
                              chr(0xfb4a))),

    ("0x05d5+0x05b9→0xfb4b", ("(0x05d5+0x05b9→0xfb4b) hebrew letter vav with holam",
                              chr(0x05d5) + chr(0x05b9),
                              chr(0xfb4b))),

    ("0x05d1+0x05bf→0xfb4c", ("(0x05d1+0x05bf→0xfb4c) hebrew letter bet with rafe",
                              chr(0x05d1) + chr(0x05bf),
                              chr(0xfb4c))),

    ("0x05db+0x05bf→0xfb4d", ("(0x05db+0x05bf→0xfb4d) hebrew letter kaf with rafe",
                              chr(0x05db) + chr(0x05bf),
                              chr(0xfb4d))),

    ("0x05e4+0x05bf→0xfb4e", ("(0x05e4+0x05bf→0xfb4e) hebrew letter pe with rafe",
                              chr(0x05e4) + chr(0x05bf),
                              chr(0xfb4e))),

    ("0xfb49+0x05c1→0xfb2c", ("(0xfb49+0x05c1→0xfb2c) hebrew letter shin with dagesh and shin dot",
                              chr(0xfb49) + chr(0x05c1),
                              chr(0xfb2c))),

    ("0xfb49+0x05c2→0xfb2d", ("(0xfb49+0x05c2→0xfb2d) hebrew letter shin with dagesh and sin dot",
                              chr(0xfb49) + chr(0x05c2),
                              chr(0xfb2d))),
    )
