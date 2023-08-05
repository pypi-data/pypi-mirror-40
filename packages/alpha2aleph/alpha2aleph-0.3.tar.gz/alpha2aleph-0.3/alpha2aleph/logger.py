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

        logger.py : logging facilities
"""
import logging
import alpha2aleph.cfgini


class LoggerPlus(logging.Logger):
    """
        LoggerPlus class
    """
    def __init__(self, name, level=logging.NOTSET):
        """
                LoggerPlus.__init__()
        """
        logging.Logger.__init__(self, name, level)

    def pipelinetrace(self, pipeline_part, msg, *args, **kwargs):
        """
                LoggerPlus.pipelinetrace()

                Call Logger.info() only if the flags defined in the cfg file
                authorize a log message.
        """
        if pipeline_part in alpha2aleph.cfgini.CFGINI["pipeline.trace"]["yes"]:
            return logging.Logger.info(self, "["+pipeline_part+"] "+msg, *args, **kwargs)

        elif pipeline_part not in alpha2aleph.cfgini.CFGINI["pipeline.trace"]["no"]:
            raise RuntimeError("Undefined pipeline part '{0}' "
                               "in the configuration file.".format(pipeline_part))

        return None
