#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os
import os.path
import sys
import re
import shutil
from functools import reduce

from zbuild.module import module_obj
from zbuild.finder import files
from zbuild import globals
from zbuild.log import logger

def __set_cmake_files(outdir):

    datadir = globals.get('datadir')

    dst_cmake_files_path = os.path.join(outdir, 'cmake_files')
    src_cmake_files_path = os.path.join(datadir, 'cmake_files')

    if os.path.exists(dst_cmake_files_path):
        shutil.rmtree(dst_cmake_files_path)
    shutil.copytree(src_cmake_files_path, dst_cmake_files_path)


    # import hashlib
    # src_cmake_files = files.get_files(src_cmake_files_path)
    # for file_path in src_cmake_files:
    #     src_cmake_file = file_path
    #     file_path = src_cmake_file.replace(src_cmake_files_path, '')
    #     dst_cmake_file = dst_cmake_files_path + file_path.rstrip('/\\')
    #     if os.path.exists(dst_cmake_file):
    #         with open(src_cmake_file, 'rb') as file:
    #             src_md5 = hashlib.md5(file.read()).hexdigest()
    #         with open(dst_cmake_file, 'rb') as file:
    #             dst_md5 = hashlib.md5(file.read()).hexdigest()
    #         if src_md5 != dst_md5:
    #             os.remove(dst_cmake_file)
    #         else:
    #             continue
    #     shutil.copyfile(src_cmake_file, dst_cmake_file)

def __list_remove_duplicates(list_data):
    func = lambda x,y:x if y in x else x + [y]
    return reduce(func, [[], ] + list_data)

def __generate_cmake_file(outdir, modules):

    logger.info("Generatimg cmake file")

    rootdir = globals.get('rootdir')
    binariesdir = globals.get('outdir') + "/binaries/" + module_obj.module_obj.platform

    __set_cmake_files(outdir)

    outpath = os.path.join(outdir, "CMakeLists.txt")
    cmake_list = open(outpath, 'w')

    slnname = globals.get('slnname')

    data_buffer = 'cmake_minimum_required(VERSION 3.10.0)\n\n'
    data_buffer += 'project(' + slnname + ')\n\n'

    data_buffer += 'include(cmake_files/version.cmake)\n'
    data_buffer += 'message(STATUS \"${PROJECT_NAME} Version: ${PROJECT_VERSION} (${PROJECT_VERSION_INT})\")\n\n'

    data_buffer += 'get_filename_component(PROJECT_ROOT_DIR \"' + rootdir.replace('\\', '/') + '\" REALPATH)\n\n'
    data_buffer += 'get_filename_component(PROJECT_BINARIES_DIR \"' + binariesdir.replace('\\', '/') + '\" REALPATH)\n\n'

    data_buffer += 'include(cmake_files/configure.cmake)\n'
    data_buffer += 'include(cmake_files/utils.cmake)\n'
    data_buffer += 'include(cmake_files/common.cmake)\n\n'

    data_buffer += 'message(STATUS \"${PROJECT_NAME} CPU archiecture = ${BUILD_CPU_ARCHITECTURE}\")\n'
    data_buffer += 'message(STATUS \"${PROJECT_NAME} platform = ${PLATFORM}\")\n'
    data_buffer += 'message(STATUS \"${PROJECT_NAME} root path: ${PROJECT_ROOT_DIR}\")\n\n'

    cmake_list.writelines(data_buffer)

    for module in modules:

        data_buffer = "# " + module.name + '\n'

        data_buffer += "add_module(\n"

        data_buffer += "    NAME\n"
        data_buffer += "        \"" + module.name + "\"\n"

        data_buffer += "    TYPE\n"
        data_buffer += "        \"" + module.type + "\"\n"

        data_buffer += "    CONFIGURATION_TYPE\n"
        data_buffer += "        \"" + module.configuration_type + "\"\n"

        data_buffer += "    ROOT_DIR\n"
        module.root_dir = module.root_dir.replace("\\", "/")
        data_buffer += "        \"" + module.root_dir + "\"\n"

        data_buffer += "    SRC_DIR\n"
        module.src_dir = module.src_dir.replace("\\", "/")
        data_buffer += "        \"" + module.src_dir + "\"\n"

        data_buffer += "    BUILD_DIR\n"
        module.build_dir = module.build_dir.replace("\\", "/")
        data_buffer += "        \"" + module.build_dir + "\"\n"

        data_buffer += "    SOURCE_FILES\n"
        source_files = __list_remove_duplicates(module.source_files)
        for source_file in source_files:
            source_file = source_file.replace("\\", "/")
            data_buffer += "        \"" + source_file + "\"\n"

        data_buffer += "    INCLUDE_PATHS\n"
        private_include_paths = __list_remove_duplicates(module.private_include_paths)
        public_include_paths = __list_remove_duplicates(module.public_include_paths)
        for include_path in private_include_paths:
            include_path = include_path.replace("\\", "/")
            data_buffer += "        \"" + include_path + "\"\n"
        for include_path in public_include_paths:
            include_path = include_path.replace("\\", "/")
            data_buffer += "        \"" + include_path + "\"\n"

        data_buffer += "    RUNTIME_DEPENDENCIES\n"
        runtime_dependencies = __list_remove_duplicates(module.runtime_dependencies)
        for runtime_dependency in runtime_dependencies:
            runtime_dependency = runtime_dependency.replace("\\", "/")
            data_buffer += "        \"" + runtime_dependency + "\"\n"

        data_buffer += "    STATIC_DEPENDENCIES\n"
        static_dependencies = __list_remove_duplicates(module.static_dependencies)
        for static_dependency in static_dependencies:
            static_dependency = static_dependency.replace("\\", "/")
            data_buffer += "        \"" + static_dependency + "\"\n"

        data_buffer += "    DEPENDENCY_MODULE_NAMES\n"
        dependency_module_names = __list_remove_duplicates(module.dependency_module_names)
        for dependency_module_name in dependency_module_names:
            data_buffer += "        \"" + dependency_module_name + "\"\n"

        data_buffer += "    PREPROCESSED_FILES\n"
        private_preprocessed_files = __list_remove_duplicates(module.private_preprocessed_files)
        for preprocessed_file in private_preprocessed_files:
            preprocessed_file = preprocessed_file.replace("\\", "/")
            data_buffer += "        \"" + preprocessed_file + "\"\n"
        public_preprocessed_files = __list_remove_duplicates(module.public_preprocessed_files)
        for preprocessed_file in public_preprocessed_files:
            data_buffer += "        \"" + preprocessed_file + "\"\n"

        data_buffer += "    DEFINITIONS\n"
        private_definitions = __list_remove_duplicates(module.private_definitions)
        for definition in private_definitions:
            data_buffer += "        \"" + definition + "\"\n"
        public_definitions = __list_remove_duplicates(module.public_definitions)
        for definition in public_definitions:
            data_buffer += "        \"" + definition + "\"\n"

        data_buffer += "    COMPILE_OPTIONS\n"
        for compile_option in module.compile_options:
            data_buffer += "        \"" + compile_option + "\"\n"

        data_buffer += "    LINK_OPTIONS\n"
        for link_option in module.link_options:
            data_buffer += "        \"" + link_option + "\"\n"

        data_buffer += ")\n\n"

        cmake_list.writelines(data_buffer)

    cmake_list.close()

def generate_cmake_file(modules):

    if len(modules) == 0:
        return

    cmake_out_dir = os.path.join(globals.get('outdir'), 'intermediate')
    cmake_out_dir = os.path.join(cmake_out_dir, 'cmake')
    if not os.path.exists(cmake_out_dir):
        os.makedirs(cmake_out_dir)

    __generate_cmake_file(cmake_out_dir, modules)
