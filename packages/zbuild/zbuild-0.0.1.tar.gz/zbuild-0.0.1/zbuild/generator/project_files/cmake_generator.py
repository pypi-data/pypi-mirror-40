#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os
import subprocess

from zbuild import globals
from .cmake import generate_file

def cmake_configure():

    srcdir = os.path.join(globals.get('outdir') + 'cmake')
    outdir = os.path.join(globals.get('outdir') + 'project_files')
    srcdir = srcdir.replace('\\', '/')
    builddir = outdir.replace('\\', '/')
    platformname = globals.get('platform')

    generate = ''
    if platformname == 'win64':
        generate = "Visual Studio 15 2017 Win64"
    elif platformname == 'win32':
        generate = "Visual Studio 15 2017"
    elif platformname == 'linux':
        generate = 'Unix Makefiles'


    cmake_command = ['\"cmake\"']

    cmake_command.append('-Wno-dev')

    cmake_command.append('-S \"' + srcdir + '\"')
    cmake_command.append('-B \"' + builddir + '\"')

    cmake_command.append('-G \"' + generate + '\"')

    print(' '.join(cmake_command))

    #ret = subprocess.call(cmake_command,shell=True)
    cmd = ' '.join(cmake_command)
    os.system("start /wait cmd /c \"" + cmd + '\"')

    # Start cmake-gui application
    # subprocess.Popen(['cmake-gui'])

def generate(modules):

    # for module in modules:
    #     print(module.name)
    #     print(module.type)
    #     print(module.dependency_ref_count)

    generate_file.generate_cmake_file(modules)
    cmake_configure()