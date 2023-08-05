#!/usr/bin/python
# -*- coding: UTF-8 -*-

class module_obj(object):
    platform = ''
    def __init__(self):

        self.exclude_dirs = ['intermediate']

        # CMAKE NAME
        self.name = ''

        # 'module' or 'external'
        self.type = 'module'

        self.configuration_type = ''

        # CMAKE DIRECTORY
        self.root_dir = ''

        self.src_dir = ''

        self.build_dir = ''

        self.copyright_info = {
            'hpp' : '// Copyright 2018-2019 Zeit, Inc. All rights reserved.',
            'cpp' : '// Copyright 2018-2019 Zeit, Inc. All rights reserved.',
            'inl' : '// Copyright 2018-2019 Zeit, Inc. All rights reserved.',
            'h' : '/*\n * Copyright 2018-2019 Zeit, Inc. All rights reserved.\n */\n',
            'c' : '/*\n * Copyright 2018-2019 Zeit, Inc. All rights reserved.\n */\n',
            'S' : '/*\n * Copyright 2018-2019 Zeit, Inc. All rights reserved.\n */\n'
        }

        # CMAKE SOURSE_FILES
        self.source_files = []

        # CMAKE INCLUDE_PATHS
        self.private_include_paths = []
        self.public_include_paths = []

        # CMAKE PREPROCESSED_FILES
        self.private_preprocessed_files = []
        self.public_preprocessed_files = []

        # CMAKE RUNTIME_DEPENDENCIES
        self.runtime_dependencies = []

        # CMAKE STATIC_DEPENDENCIES
        self.static_dependencies = []

        # CMAKE DEFINITIONS
        self.public_definitions = []
        self.private_definitions = []

        # CMAKE DEPENDENCY_MODULE_NAMES
        self.dependency_module_names = []

        self.include_path_module_names = []

        # CMAKE PRIVATE_THIRD_PARTY_DEPENDENCIES
        self.public_third_party_dependencies = []
        self.private_third_party_dependencies = []

        self.compile_options = []
        self.link_options = []

        # dependency ref count
        self.dependency_ref_count = 0