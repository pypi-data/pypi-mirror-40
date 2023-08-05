#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os
import sys
import json
import re
import copy

from zbuild import globals
from zbuild.log import logger
from zbuild.module import module_obj
from zbuild.finder import files

from . import _load_source

def __get_module_source_files(directory, exclude_dirs, platformname):

    platformnames = ['linux', 'windows', 'mac']
    if platformname == 'win64' or platformname == 'win32':
        platformname = 'windows'

    regex_str = ''
    if (len(exclude_dirs) > 0):
        regex_str = '.*?('
        for exclude_dir in exclude_dirs:
            regex_str += exclude_dir + '|'
        regex_str = regex_str.strip('|')
        regex_str += ')+.*?'

    module_source_files = []
    source_files = files.get_files(directory)
    for source_file in source_files:
        if re.match(regex_str, source_file):
            continue
        can_append = True
        for name in platformnames:
            if name in source_file and name != platformname:
                can_append = False
                break
        if can_append:
            module_source_files.append(source_file)
    return module_source_files

def __parse_module(module):

    if module.type == '':
        logger.error('Module not set type!')
        return False

    if module.root_dir == '':
        logger.error('Module not set root directory!')
        return False

    module.build_dir = globals.get('outdir')
    if module.build_dir == '':
        logger.error('Module not set build directory!')
        return False

    if module.configuration_type == '':
        return True

    source_files = __get_module_source_files(module.src_dir, module.exclude_dirs, module.platform)
    if len(source_files) == 0:
        logger.info('Module no source files!')
        return False

    module.source_files.extend(source_files)

    for source_file in module.source_files:
        file_ext = os.path.splitext(source_file)[1].strip('.')
        if not module.copyright_info.get(file_ext, None):
            continue
        copyright_info = module.copyright_info[file_ext]
        copyright_info_len = len(copyright_info)
        copyright_info_file = open(source_file, 'r')
        file_data = copyright_info_file.read(copyright_info_len)
        copyright_info_file.close()
        if copyright_info != file_data:
            print(file_data)
            print("\"" + source_file +  "\" file not copyright info.")
            print("Need copyright info:")
            print(copyright_info)
            exit(-1)

    return True

def parse_project_files(build_files):

    module_obj.module_obj.platform = globals.get('platform')

    modules = []
    for build_file in build_files:
        logger.debug('Building ' + build_file + '.')
        file_dir = os.path.abspath(os.path.dirname(build_file))
        functions = _load_source.load_source('', build_file).functions
        for func in functions:
            module = module_obj.module_obj()
            module.root_dir = file_dir
            module.source_files.append(build_file)
            func(module)
            if __parse_module(module):
                logger.info('Build ' + module.name + ' succeed.')
                modules.append(module)
            else:
                logger.info('Build ' + module.name + ' failed.')
        logger.debug('Build end.')

    return modules
