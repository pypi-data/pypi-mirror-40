#!/usr/bin/python
# -*- coding: UTF-8 -*-

import sys
import os

from .log import logger
from .generator import project_files_generator

from . import globals

def main():

    if len(sys.argv) != 5:
        print(sys.argv)
        print("zbuild [slnname] [rootdir] [outdir] [platformname]")
        return

    globals.set('slnname', sys.argv[1])
    globals.set('rootdir', sys.argv[2].rstrip('/\\'))
    globals.set('outdir', sys.argv[3].rstrip('/\\'))
    globals.set('platform', sys.argv[4])
    datadir = os.path.dirname(__file__) + '/data'
    globals.set('datadir', datadir.rstrip('/\\').replace('\\', '/'))

    if globals.get('platform') not in ["win64", "win32", "linux", "mac"]:
        print('platformname not win64, win32, linux and mac!')
        return

    logger.initialise('c', globals.get('outdir'))
    project_files_generator.generate('cmake')

if __name__== '__main__':
    main()
