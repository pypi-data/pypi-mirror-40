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

        cmdline.py : read_command_line_arguments() function
"""
import argparse

from .glob import __projectname__, __version__, \
                  __license__, __author__, __email__


def read_command_line_arguments():
    """
        read_command_line_arguments()
        ________________________________________________________________________

        Read the command line arguments.
        ________________________________________________________________________

        no PARAMETER

        RETURNED VALUE
                return the argparse object.
    """
    parser = argparse.ArgumentParser(description="{0} v. {1}".format(__projectname__, __version__),
                                     epilog="{0} v. {1} ({2}), a project by {3} "
                                            "({4})".format(__projectname__,
                                                           __version__,
                                                           __license__,
                                                           __author__,
                                                           __email__),
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('--log',
                        choices=['DEBUG', 'INFO', 'ERROR', 'CRITICAL'],
                        default="INFO",
                        help="set log level")

    parser.add_argument('--version',
                        action="store_true",
                        help="show version number and exit")

    parser.add_argument('--about',
                        action="store_true",
                        help="show informations about the version, license, author and exit")

    parser.add_argument('--downloadbasics',
                        action="store_true",
                        help="download basic files like default symbols.txt "
                             "and config.ini, and exit")

    parser.add_argument('--checksymbols',
                        action="store_true",
                        help="check symbols coherency and exit")

    parser.add_argument('--explicitsymbols',
                        action="store_true",
                        help="explicit symbols, displaying unicode analyse of each character")

    parser.add_argument('--explicitoutput',
                        action="store_true",
                        help="explicit output string, displaying unicode analyse of each character")

    parser.add_argument('--transform_alpha2alephrew',
                        choices=['yes', 'no'],
                        default="yes",
                        help="if 'no', do not read the input file, do not transform it")

    parser.add_argument('--inputfile',
                        type=str,
                        default="input.txt",
                        help="name of the inputfile to be read and transformed")

    parser.add_argument('--symbolsfile',
                        type=str,
                        default="symbols.txt",
                        help='name of the symbols file to be read')

    parser.add_argument('--outputformat',
                        choices=['html', 'console'],
                        default="console",
                        help="output format")

    parser.add_argument("--cfgfile",
                        type=str,
                        default="config.ini",
                        help="name of the configuration file to be read")

    parser.add_argument("--checkinputdata",
                        choices=['yes', 'no'],
                        default="yes",
                        help="if 'yes', check the coherency of the input data")

    parser.add_argument("--source",
                        choices=['stdin', 'inputfile'],
                        default="inputfile",
                        help="choose 'stdin' to use the script through a pipe")

    return parser.parse_args()
