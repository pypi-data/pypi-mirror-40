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

        main.py : entry point in the project.
"""
import logging
import re
import sys
import os
import os.path
import urllib.request
import shutil

import alpha2aleph.logger

import alpha2aleph.globalsrtl
from alpha2aleph.regex import get_rtlreader_regex

from alpha2aleph.fb1d_fb4f import TRANSF_FB1D_FB4F
from alpha2aleph.utils import stranalyse, match_repr, extracts, extract_around_index, normpath
from alpha2aleph.cmdline import read_command_line_arguments
from alpha2aleph.improve_rtlalphatext import IMPROVE_RTLALPHATEXT

from .glob import __projectname__, __version__, __license__, __author__, __location__, LOGGING_LEVEL

from .logger import LoggerPlus


# let's try to import pyfribidi :
PYFRIBIDI_AVAILABLE = True
try:
    import pyfribidi
except ModuleNotFoundError as err:
    PYFRIBIDI_AVAILABLE = False


def add_firstlast_markers(src):
    """
       add_firstlast_markers()
       ________________________________________________________________________

       Add to (str)src a first and a last character.

       see remove_firstlast_markers()
       ________________________________________________________________________

       PARAMETER      : (str)src

       RETURNED VALUE : (str)the resulting string
    """
    logger = alpha2aleph.glob.LOGGER

    # remark about logger and pipelinetrace():
    # ˮno id number for messages given to logger.pipelinetrace(), e.g. no "[I01]"
    logger.pipelinetrace("add_firstlast_markers",
                         "add markers for the first and last characters")
    return "$"+src+"$"


def remove_firstlast_markers(src):
    """
       remove_firstlast_markers()
       ________________________________________________________________________

       Remove from (str)src its first last character, normally the characters
       added by a call to add_firstlast_markers().
       ________________________________________________________________________

       PARAMETER      : (str)src

       RETURNED VALUE : (str)the resulting string
    """
    logger = alpha2aleph.glob.LOGGER

    # remark about logger and pipelinetrace():
    # ˮno id number for messages given to logger.pipelinetrace(), e.g. no "[I01]"
    logger.pipelinetrace("remove_firstlast_markers",
                         "remove markers for the first and last characters")
    return src[1:-1]


def replace_and_log(pipeline_part, comment, src, before_after):
    """
       replace_and_log()
       ________________________________________________________________________

       simply return src.replace(before, after) but with a log message
       ________________________________________________________________________

       PARAMETERS     : (str)pipeline_part
                        (str)comment
                        (str)src
                        (str, str)before_after

       RETURNED VALUE : (str)the resulting string, namely src.replace(before, after)
    """
    logger = alpha2aleph.glob.LOGGER

    before, after = before_after

    if before in src:
        # remark about logger and pipelinetrace():
        # ˮno id number for messages given to logger.pipelinetrace(), e.g. no "[I01]"
        logger.pipelinetrace(pipeline_part,
                             "%s : '%s' > '%s' in %s",
                             comment, before, after, extracts(before, src))
        return src.replace(before, after)

    logger.debug("[D02] Nothing to do in '%s' for %s : '%s' > '%s' in \"%s\"",
                 src, comment, before, after, extracts(before, src))
    return src


def sub_and_log(cfgini_flag, pipeline_part, comment, before_after, src):
    """
       sub_and_log()
       ________________________________________________________________________

       simply return re.sub(before, after, src) with a log message if
       cfgini_flag.lower() == "true".
       ________________________________________________________________________

       PARAMETERS     : (str)cfgini_flag
                        (str)pipeline_part
                        (str)comment
                        (str)src
                        (str, str)before_after
                        (str)src

       RETURNED VALUE : (str)the resulting string, namely src.replace(before, after)
    """
    logger = alpha2aleph.glob.LOGGER

    before, after = before_after

    if cfgini_flag.lower() != "true":
        logger.debug("[D03] Nothing to do in '%s' for %s : '%s' > '%s' in %s",
                     src, comment, before, after, extracts(before, src))

    if before in src:
        # remark about logger and pipelinetrace():
        # ˮno id number for messages given to logger.pipelinetrace(), e.g. no "[I01]"
        logger.pipelinetrace(pipeline_part,
                             "%s : '%s' > '%s' in '%s'",
                             comment, before, after, extracts(before, src))
        return re.sub(before, after, src)

    logger.debug("[D04] Nothing to do in '%s' for %s : '%s' > '%s' in %s",
                 src, comment, before, after, extracts(before, src))

    return src


def read_symbols(filename):
    """
       read_symbols()
       ________________________________________________________________________

       Read the symbol file <filename> and return the dict of keys → value
       ________________________________________________________________________

       PARAMETERS     : (str)filename

       RETURNED VALUE : (success,
                         errors,
                         alpha2alephrew,
                         sorted(keys_in_alpha2alephrew))
    """
    logger = alpha2aleph.glob.LOGGER

    logger.debug("[D05] read_symbols : '%s'", filename)

    if not os.path.exists(filename):
        return (False,
                ["Where is symbols file '{0}', namely '{1}' ?".format(filename,
                                                                      normpath(filename))],
                None,
                None)

    success = True
    errors = []

    alpha2alephrew = dict()
    with open(filename) as symbols:
        for line_index, _line in enumerate(symbols.readlines()):
            line = _line.strip()

            if '#' in line:
                line = line[:line.index('#')]
                line = line.strip()

            if line != "":
                if '→' in line:
                    alpha, hebrew = line.split("→")
                    alpha = alpha.strip()
                    hebrew = hebrew.strip()
                    if alpha in alpha2alephrew:
                        errors.append("key '{0}' has alread been defined; "
                                      "new definition in line {1} (line #{2})".format(alpha,
                                                                                      line,
                                                                                      line_index))
                        success = False
                    alpha2alephrew[alpha] = hebrew

    keys = sorted(alpha2alephrew.keys(), key=len, reverse=True)

    if not keys:
        success = False
        errors.append("empty alpha2alephrew dict")

    return success, errors, alpha2alephrew, keys


def transf__text_alpha2alephrew(_src):
    """
       transf__text_alpha2alephrew()
       ________________________________________________________________________

       Convert the text <_src>, written using some alphabetic symbols, in
       a translitterated text written in hebrew.
       ________________________________________________________________________

       PARAMETERS     : (str)_src, the text to be translitterated.
                        _src is a string so that rtl_begin+_src+rtl_end
                        is the original string.

       RETURNED VALUE : (str)the translitterated text with RTL symbols added
                        at the beginning and at the end.
    """
    logger = alpha2aleph.glob.LOGGER

    src = _src.group("rtltext")

    for alphachar in alpha2aleph.logger.ALPHA2HEBREW_KEYS:
        src = replace_and_log("transf__text_alpha2alephrew",
                              "[transf__text_alpha2alephrew]",
                              src, (alphachar, alpha2aleph.logger.ALPHA2HEBREW[alphachar]))

    # remark about logger and pipelinetrace():
    # ˮno id number for messages given to logger.pipelinetrace(), e.g. no "[I01]"
    logger.pipelinetrace("transf__text_alpha2alephrew",
                         "Adding globals.RTL_SYMBOLS to '%s' : '%s' and '%s'",
                         src,
                         alpha2aleph.globalsrtl.RTL_SYMBOLS[0],
                         alpha2aleph.globalsrtl.RTL_SYMBOLS[1])

    return alpha2aleph.globalsrtl.RTL_SYMBOLS[0]+src+alpha2aleph.globalsrtl.RTL_SYMBOLS[1]


def transf__improve_rtlalphatext(src):
    """
       transf__improve_rtlalphatext()
       ________________________________________________________________________

       Modify the source string <src> using different calls to sub_and_log().
       The calls are defined by IMPROVE_RTLALPHATEXT.
       ________________________________________________________________________

       PARAMETERS     : (str)_src

       RETURNED VALUE : (str) _src through several calls to sub_and_log().
    """
    for (_cfgini_flag,
         pipeline_part,
         comment,
         before,
         after) in IMPROVE_RTLALPHATEXT:

        cfgini_flag = alpha2aleph.cfgini.CFGINI["pipeline.improve rtlalphatext"][_cfgini_flag]
        src = sub_and_log(cfgini_flag, pipeline_part, comment, (before, after), src)

    return src


def transf__invert_rtltext(src):
    """
       transf__invert_rtltext()
       ________________________________________________________________________

       Invert src : "abc" becoming "cba"
       ________________________________________________________________________

       PARAMETERS     : (_sre.SRE_Match)src, the source match object.

       RETURNED VALUE : (str)_src.group("rtltext")[::-1] with RTL symbols
                        before/after.
    """
    logger = alpha2aleph.glob.LOGGER

    res = src.group("rtltext")[::-1]
    res = alpha2aleph.globalsrtl.RTL_SYMBOLS[0]+res+alpha2aleph.globalsrtl.RTL_SYMBOLS[1]

    # remark about logger and pipelinetrace():
    # ˮno id number for messages given to logger.pipelinetrace(), e.g. no "[I01]"
    logger.pipelinetrace("transf__invert_rtltext",
                         "inverting the text : '%s' > '%s'",
                         match_repr(src), res)

    return res


def transf__use_fb1d_fb4f_chars(_src):
    """
       transf__use_fb1d_fb4f_chars()
       ________________________________________________________________________

       Modify the source string <_src> using different calls to replace_and_log()
       in order to replace some characters by those defined in the Unicode range
       0xFB1D to 0xFB4F.
       The calls are defined by fb1d_fb4f.TRANSF_FB1D_FB4F .
       The calls are controlled by the configuration file, section "pipeline.use FB1D-FB4F chars".
       ________________________________________________________________________

       PARAMETERS     : (str)_src, the source string

       RETURNED VALUE : (str)the resulting string.
    """
    logger = alpha2aleph.glob.LOGGER

    src = _src.group("rtltext")

    # ---- 1/2 FB1D-FB4F characters : ----
    for _, (fullname, before, after) in TRANSF_FB1D_FB4F:

        if alpha2aleph.cfgini.CFGINI["pipeline.use FB1D-FB4F chars"][fullname].lower() == "true":
            pipeline_part = "transf__use_fb1d_fb4f_chars"
            comment = "{0}::{1}".format("transf__use_fb1d_fb4f_chars",
                                        fullname)
            src = replace_and_log(pipeline_part, comment, src, (before, after))

    # ---- 2/2 let's add the first/last chars removed by calling this function ----
    # remark about logger and pipelinetrace():
    # ˮno id number for messages given to logger.pipelinetrace(), e.g. no "[I01]"
    logger.pipelinetrace("transf__use_fb1d_fb4f_chars",
                         "Adding alpha2aleph.globalsrtl.RTL_SYMBOLS to '%s' : '%s' and '%s'",
                         src,
                         alpha2aleph.globalsrtl.RTL_SYMBOLS[0],
                         alpha2aleph.globalsrtl.RTL_SYMBOLS[1])

    return alpha2aleph.globalsrtl.RTL_SYMBOLS[0]+src+alpha2aleph.globalsrtl.RTL_SYMBOLS[1]


def output_html(inputdata):
    """
       output_html()
       ________________________________________________________________________

       Make an html output from the <inputdata>.
       ________________________________________________________________________

       PARAMETERS     : (str)inputdata, the source string.

       RETURNED VALUE : (str)the result string.
    """
    logger = alpha2aleph.glob.LOGGER

    logger.debug("[D06] [output_html] : data to be read=%s", inputdata)

    rtl_start = '<span class="rtltext" dir="rtl">'
    rtl_end = '</span>'

    header = []
    header.append("<!DOCTYPE html>")
    header.append("")
    header.append("<html>")
    header.append("")
    header.append("<head>")
    header.append("    <title>Page Title</title>")
    header.append('    <meta http-equiv="content-type" content="text/html; charset=utf-8" />')
    header.append("    <style>")
    header.append("        body {")
    header.append('          {0}'.format(alpha2aleph.cfgini.CFGINI["output.html"]["body"]))
    header.append("          }")
    header.append("")
    header.append("        .rtltext {")
    header.append('          {0}'.format(alpha2aleph.cfgini.CFGINI["output.html"]["rtltext"]))
    header.append("        }")
    header.append("    </style>")
    header.append("</head>")
    header.append("")
    header.append("<body>")
    header.append("")
    header = "\n".join(header)

    # transformation html.1::text_delimiters
    #    let's add a char at the very beginning and at the very end of the
    #    source string.
    outputdata = add_firstlast_markers(inputdata)

    # transformation html.2::maingroup
    outputdata = transf__maingroup(outputdata)

    # transformation html.3::br
    outputdata = outputdata.replace("\n", "<br/>\n")

    # transformation html.4::RTL_SYMBOLS
    outputdata = outputdata.replace(alpha2aleph.globalsrtl.RTL_SYMBOLS[0], rtl_start)
    outputdata = outputdata.replace(alpha2aleph.globalsrtl.RTL_SYMBOLS[1], rtl_end)

    # transformation html.5::undo_text_delimiters
    #    see transformation html.1::text_delimiters
    outputdata = remove_firstlast_markers(outputdata)

    foot = []
    foot.append("")
    foot.append("</body>")
    foot.append("")
    foot.append("</html>")
    foot = "\n".join(foot)

    return header + outputdata + foot


def output_console(inputdata):
    """
       output_html()
       ________________________________________________________________________

       Make a console output from the <inputdata>.
       ________________________________________________________________________

       PARAMETERS     : (str)inputdata, the source string.

       RETURNED VALUE : (str)the result string.
    """
    logger = alpha2aleph.glob.LOGGER

    logger.debug("[D07] [output_console] : data to be read=%s", inputdata)

    # transformation console.1::text_delimiters
    #    let's add a char at the very beginning and at the very end of the
    #    source string.
    outputdata = add_firstlast_markers(inputdata)

    # transformation console.2::maingroup
    outputdata = transf__maingroup(outputdata)

    # transformation console.3::invert_rtltext
    if alpha2aleph.cfgini.CFGINI["output.console"]["invert_rtltext"].lower() == 'true':
        outputdata = re.sub(alpha2aleph.globalsrtl.RTLREADER_REGEX,
                            transf__invert_rtltext,
                            outputdata)

    # transformation console.4::remove_RTL_SYMBOLS
    # https://en.wikipedia.org/wiki/Bi-directional_text
    if alpha2aleph.cfgini.CFGINI["output.console"]["rtl symbols"].lower() == "0x200f_0x200e":
        outputdata = outputdata.replace(alpha2aleph.globalsrtl.RTL_SYMBOLS[0], chr(0x200F))
        outputdata = outputdata.replace(alpha2aleph.globalsrtl.RTL_SYMBOLS[1], chr(0x200E))

    elif alpha2aleph.cfgini.CFGINI["output.console"]["rtl symbols"].lower() == "empty string":
        outputdata = outputdata.replace(alpha2aleph.globalsrtl.RTL_SYMBOLS[0], "")
        outputdata = outputdata.replace(alpha2aleph.globalsrtl.RTL_SYMBOLS[1], "")

    # transformation console.5::undo_text_delimiters
    outputdata = remove_firstlast_markers(outputdata)

    # transformation console.6::use fribidi
    if alpha2aleph.cfgini.CFGINI["output.console"]["use fribidi"].lower() == "true":
        if PYFRIBIDI_AVAILABLE:
            outputdata = pyfribidi.log2vis(outputdata)
        else:
            logger.error("[E01] You can't use fribidi : this library seems not to be installed.")

    return outputdata


def transf__maingroup(src):
    """
       output_html()
       ________________________________________________________________________

       Modify the source string <src> using different calls to various
       functions.
       ________________________________________________________________________

       PARAMETERS     : (str)src, the source string.

       RETURNED VALUE : (str)the result string.
    """
    logger = alpha2aleph.glob.LOGGER

    logger.debug("[D08] transf__maingroup()")

    # transformation maingroup.1::improve_rtlalphatext
    src = transf__improve_rtlalphatext(src)

    # transformation maingroup.2::transf__text_alpha2alephrew
    src = re.sub(alpha2aleph.globalsrtl.RTLREADER_REGEX, transf__text_alpha2alephrew, src)

    # transformation maingroup.3::transf__use_fb1d_fb4f_chars
    src = re.sub(alpha2aleph.globalsrtl.RTLREADER_REGEX, transf__use_fb1d_fb4f_chars, src)

    return src


def check_inputdata(inputdata):
    """
       check_inputdata()
       ________________________________________________________________________

       Check the coherency of <inputdata>.
       ________________________________________________________________________

       PARAMETERS     : (str)inputdata, the source string.

       RETURNED VALUE : (bool)ok, (list of str)errors
    """
    logger = alpha2aleph.glob.LOGGER

    logger.debug("[D09] check_inputdata()")

    rtl_start, rtl_end = alpha2aleph.globalsrtl.RTL_SYMBOLS

    success = True
    errors = []

    # ------------------------------------------------------------------------
    # ---- a special case : no check if RTL_SYMBOLS[0]==RTL_SYMBOLS[1]
    # ------------------------------------------------------------------------
    if rtl_start == rtl_end:
        return True, []

    # ------------------------------------------------------------------------
    # ---- common case : RTL_SYMBOLS[0] != RTL_SYMBOLS[1]
    # ------------------------------------------------------------------------
    # first check : is num_of(globals.RTL_SYMBOLS[0]) equal to num_of(globals.RTL_SYMBOLS[1]) ?
    if inputdata.count(rtl_start) != inputdata.count(rtl_end):
        success = False
        errors.append("Not even numbers of symbols '{0}' and '{1}'".format(rtl_start, rtl_end))

    # second check : no two globals.RTL_SYMBOLS[x] twice in a row
    # third check : first RTL_SYMBOL must be globals.RTL_SYMBOLS[0]
    last_symbol = None
    for line_number, line in enumerate(inputdata):
        for char_number, char in enumerate(line):
            _extract = extract_around_index(line,
                                            char_number)
            context = 'line #{0}::character {1} (\"{2}\")'.format(line_number+1,
                                                                  char_number+1,
                                                                  _extract)

            if char in alpha2aleph.globalsrtl.RTL_SYMBOLS:
                if last_symbol is None:
                    if char == alpha2aleph.globalsrtl.RTL_SYMBOLS[1]:
                        errors.append("first RTL_SYMBOL must be {0}, "
                                      "not {1} (context={2})".format(rtl_start, rtl_end, context))
                        success = False
                    else:
                        last_symbol = char
                else:
                    if last_symbol == char:
                        logger.error("[E02] the symbol '%s' appears two times in a row "
                                     "(context=%s)",
                                     char, context)
                        success = False
                    last_symbol = char

    return success, errors


def cmdline__downloadbasics():
    """
        cmdline__downloadbasics()
        ________________________________________________________________________

        Download the default configuration file and save them in the current
        directory.

        This function is what execute the --downloadbasics command line option.
        ________________________________________________________________________

        no PARAMETER

        RETURNED VALUE :
            (bool) success
    """
    logger = alpha2aleph.glob.LOGGER

    success = True

    for filename, url in (('config.ini', 'https://raw.githubusercontent.com/'
                                         'suizokukan/alpha2aleph/master/examples/config.ini'),
                          ('symbols.txt', 'https://raw.githubusercontent.com/'
                                          'suizokukan/alpha2aleph/master/examples/symbols.txt')):
        try:
            with urllib.request.urlopen(url) as response, \
                 open(filename, 'wb') as out_file:
                shutil.copyfileobj(response, out_file)

                # remark about logger and pipelinetrace():
                # ˮno id number for messages given to logger.pipelinetrace(), e.g. no "[I01]"
                logger.info("Downloaded '%s' as '%s'", filename, normpath(filename))

        except urllib.error.URLError as exception:
            logger.error("[E03] An error occured while downloading '%s' (url: '%s') : %s",
                         filename, url, exception)
            success = False

    return success


def cmdline__check_symbols(forcedparameters, args):
    """
        cmdline__check_symbols()
        ________________________________________________________________________

        Check the content of the symbols file.

        This function is what execute the --checksymbols command line option.
        ________________________________________________________________________

        PARAMETERS: - forcedparameters: see below
                    - args : command line arguments

        about forced parameters:
        ˮeither None, either a list of strings (cfgfile, symbolsfile, inputdata, "console|html").
        ˮif None, all the values (cfgfile, symbolsfile, ...) will be read from the command line

        RETURNED VALUE :
            (bool) success
    """
    return cmdline__read_symbols_file(forcedparameters, args)


def cmdline__read_cfg_file(forcedparameters, args):
    """
        cmdline__read_cfg_file()
        ________________________________________________________________________

        Read the configuration file and initialize alpha2aleph.cfgini.CFGINI

        This function is what execute the --cfgfile command line option.
        ________________________________________________________________________

        PARAMETERS: - forcedparameters: see below
                    - args : command line arguments

        about forced parameters:
        ˮeither None, either a list of strings (cfgfile, symbolsfile, inputdata, "console|html").
        ˮif None, all the values (cfgfile, symbolsfile, ...) will be read from the command line

        RETURNED VALUE :
            (bool) success
    """
    logger = alpha2aleph.glob.LOGGER

    if forcedparameters is None:
        (cfgini_success,
         cfgerrors,
         alpha2aleph.cfgini.CFGINI) = alpha2aleph.cfgini.read_cfg_file(args.cfgfile)

        if not cfgini_success:
            logger.error("[E04] problem with the config file '%s' : %s", args.cfgfile, cfgerrors)
            logger.error("[E05] === program stops ===")
            sys.exit(-1)

    else:
        (cfgini_success,
         cfgerrors,
         alpha2aleph.cfgini.CFGINI) = alpha2aleph.cfgini.read_cfg_file(forcedparameters[0])
        if not cfgini_success:
            return False

    return True


def cmdline__misceallenous(forcedparameters, args):
    """
        cmdline__misceallenous()
        ________________________________________________________________________

        This function is what execute the following command line options:

        --version, --about, --downloadbasics, --checksymbols
        ________________________________________________________________________

        PARAMETERS: - forcedparameters: see below
                    - args : command line arguments

        about forced parameters:
        ˮeither None, either a list of strings (cfgfile, symbolsfile, inputdata, "console|html").
        ˮif None, all the values (cfgfile, symbolsfile, ...) will be read from the command line

        RETURNED VALUE : True if something has been done, False otherwise.
    """
    if forcedparameters is None:
        if args.version:
            print(__version__)
            return True

        if args.about:
            print("{0} v. {1} by {2} : see {3}; a {4} project".format(__projectname__,
                                                                      __version__,
                                                                      __author__,
                                                                      __location__,
                                                                      __license__))
            return True

        if args.downloadbasics:
            cmdline__downloadbasics()
            return True

        if args.checksymbols:
            cmdline__check_symbols(forcedparameters, args)
            return True

    return False


def cmdline__read_symbols_file(forcedparameters, args):
    """
        cmdline__read_symbols_file()
        ________________________________________________________________________

        Read the symbols file and initialize alpha2aleph.logger.ALPHA2HEBREW and
        alpha2aleph.logger.ALPHA2HEBREW_KEYS .

        This function is what execute the --symbolsfile command line option.
        ________________________________________________________________________

        PARAMETERS: - forcedparameters: see below
                    - args : command line arguments

        about forced parameters:
        ˮeither None, either a list of strings (cfgfile, symbolsfile, inputdata, "console|html").
        ˮif None, all the values (cfgfile, symbolsfile, ...) will be read from the command line

        RETURNED VALUE :
            (bool) success
    """
    logger = alpha2aleph.glob.LOGGER

    if forcedparameters is None:
        (readsymbols_success,
         readsymbols_errors,
         alpha2aleph.logger.ALPHA2HEBREW,
         alpha2aleph.logger.ALPHA2HEBREW_KEYS) = read_symbols(args.symbolsfile)

        if not readsymbols_success:
            logger.error("[E06] problem with the symbols file '%s' : %s",
                         args.symbolsfile, readsymbols_errors)
            logger.error("[E07] === program stops ===")
            sys.exit(-3)

    else:
        (readsymbols_success,
         readsymbols_errors,
         alpha2aleph.logger.ALPHA2HEBREW,
         alpha2aleph.logger.ALPHA2HEBREW_KEYS) = read_symbols(forcedparameters[1])
        if not readsymbols_success:
            return False

    if forcedparameters is None:
        if args.showsymbols:
            for key in alpha2aleph.logger.ALPHA2HEBREW_KEYS:
                print(stranalyse(key), "---→", stranalyse(alpha2aleph.logger.ALPHA2HEBREW[key]))

    return True


def cmdline__read_inputdata(forcedparameters, args):
    """
        cmdline__read_inputdata()
        ________________________________________________________________________

        Read the input data, either from a file, either from the command
        line.

        This function is what execute the --inputfile/--source command line options.
        ________________________________________________________________________

        PARAMETERS: - forcedparameters: see below
                    - args : command line arguments

        about forced parameters:
        ˮeither None, either a list of strings (cfgfile, symbolsfile, inputdata, "console|html").
        ˮif None, all the values (cfgfile, symbolsfile, ...) will be read from the command line

        RETURNED VALUE :
            (bool) success, (str)inputdata
    """
    logger = alpha2aleph.glob.LOGGER

    inputdata = ""
    success = True

    if forcedparameters is None:
        if args.source == "inputfile":
            if not os.path.exists(args.inputfile):
                logger.error("[E08] Where is input file '%s', namely '%s' ?",
                             args.inputfile, normpath(args.inputfile))
                logger.error("[E09] === program stops ===")
                sys.exit(-4)
            else:
                with open(args.inputfile) as inputfile:
                    inputdata = inputfile.readlines()
        elif args.source == "stdin":
            inputdata = sys.stdin.read()
            if inputdata[-1] == "\n":
                inputdata = inputdata[:-1]
    else:
        inputdata = forcedparameters[2]

    if forcedparameters is None:
        if args.checkinputdata == 'yes':
            check_success, check_errors = check_inputdata(inputdata)
            if not check_success:
                logger.error("[E10] Ill-formed input data '%s'; error(s)=%s",
                             args.cfgfile, check_errors)
                logger.error("[E11] === program stops ===")
                sys.exit(-2)
            success = success and check_success

    return success, inputdata


def entrypoint(forcedparameters=None):
    """
        entrypoint()
        ________________________________________________________________________

        main entry point into alpha2aleph.
        ________________________________________________________________________

        PARAMETER: forcedparameters: see above

        returned value : a str if no error occured, None otherwise
    """
    # --------------------------------------
    # ---- (0/5) command line arguments ----
    # --------------------------------------
    if forcedparameters is None:
        args = read_command_line_arguments()

        logging.setLoggerClass(LoggerPlus)
        loggerformat = '%(levelname)-8s %(message)s'
        logging.basicConfig(format=loggerformat, level=args.log)
        alpha2aleph.glob.LOGGER = logging.getLogger(__name__)
    else:
        args = None

        logging.setLoggerClass(LoggerPlus)
        loggerformat = '%(levelname)-8s %(message)s'
        logging.basicConfig(format=loggerformat, level=LOGGING_LEVEL)
        alpha2aleph.glob.LOGGER = logging.getLogger(__name__)

    # ----------------------------------------------------
    # ---- (1/5) --version, --about, --downloadbasics ----
    # ----------------------------------------------------
    if cmdline__misceallenous(forcedparameters, args):
        sys.exit(0)

    alpha2aleph.globalsrtl.RTLREADER_REGEX = get_rtlreader_regex()

    # ----------------------------------
    # ---- (2/5) configuration file ----
    # ----------------------------------
    if not cmdline__read_cfg_file(forcedparameters, args):
        return None

    # ----------------------------
    # ---- (3/5) symbols file ----
    # ----------------------------
    if not cmdline__read_symbols_file(forcedparameters, args):
        return None

    # -----------------------------------
    # ---- (4/5) input data reading  ----
    # -----------------------------------
    success, inputdata = cmdline__read_inputdata(forcedparameters, args)
    if not success:
        return None

    # ----------------------------------------
    # ---- (5/5) input data > output data ----
    # ----------------------------------------
    res = None
    if forcedparameters is None:
        if args.transform_alpha2alephrew == 'yes':
            if args.outputformat == 'console':
                res = output_console("".join(inputdata))
                print(res)
            if args.outputformat == 'html':
                res = output_html("".join(inputdata))
                print(res)
    else:
        if forcedparameters[3] == "console":
            res = output_console("".join(inputdata))
        elif forcedparameters[3] == "html":
            res = output_html("".join(inputdata))

    return res


if __name__ == '__main__':
    entrypoint()
