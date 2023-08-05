#!/usr/bin/python
# -*- coding: UTF-8 -*-

import logging
import os.path
import sys
import time

_logger = logging.getLogger("zbuild")
_formatter = logging.Formatter("[%(asctime)s:%(msecs)d][%(levelname)s]: %(message)s", datefmt="%Y.%m.%d-%H.%M.%S")

def initialise(type = '', outputdir = None):
    if len(type) == 0 or len(type) > 2:
        return
    _logger.setLevel(logging.DEBUG)
    if type[0] == 'f':
        rq = time.strftime('%Y.%m.%d-%H.%M.%S', time.localtime(time.time()))
        outputdir = outputdir + '/logs'
        if not os.path.exists(outputdir):
            os.makedirs(outputdir)
        logfile = outputdir + '/zbuild-' + rq + '.log'
        _file_channel = logging.FileHandler(logfile, mode='w')
        _file_channel.setFormatter(_formatter)
        _logger.addHandler(_file_channel)

    if type[len(type) - 1] == 'c' :
        _console_channel = logging.StreamHandler(sys.stdout)
        _console_channel.setFormatter(_formatter)
        _logger.addHandler(_console_channel)

def debug(msg, *args, **kwargs):
    _logger.debug(msg, *args, **kwargs)

def info(msg, *args, **kwargs):
    _logger.info(msg, *args, **kwargs)

def waring(msg, *args, **kwargs):
    _logger.waring(msg, *args, **kwargs)