#!/usr/bin/python
# -*- coding: UTF-8 -*-

from zbuild.finder import files
from zbuild.log import logger
from zbuild.module import module_obj
from zbuild import globals

from .project_files import cmake_generator
from . import _parse
from . import _generate_modules

def generate(type):
    build_files = files.get_files(globals.get('rootdir'), r'.zproj')
    modules = _parse.parse_project_files(build_files)

    generate_modules = _generate_modules.get_generate_modules(modules)
    if (len(generate_modules) == 0):
        return

    if type == 'cmake':
        cmake_generator.generate(generate_modules)