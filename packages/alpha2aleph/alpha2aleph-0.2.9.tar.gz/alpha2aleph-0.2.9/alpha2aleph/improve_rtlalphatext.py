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

        improve_rtlalphatext.py : definition of the IMPROVE_RTLALPHATEXT.
"""
IMPROVE_RTLALPHATEXT = (("final kaf",
                         "transf__improve_rtlalphatext",
                         "final kaf",
                         "ḵ[:|ə](?P<ponctuation>)", "ḵ²:\\g<ponctuation>"),

                        ("alef + holam > alef + point_on_right",
                         "transf__improve_rtlalphatext",
                         "alef + holam > alef + point_on_right",
                         "Aô", "A°"),

                        ("ḥe + holam + shin > ḥe + shin",
                         "transf__improve_rtlalphatext",
                         "ḥe + holam + shin > ḥe + shin",
                         "[H|ḥ|ħ|ẖ](?P<accent>[<])?ôš", "ḥ\\g<accent>š"),)
