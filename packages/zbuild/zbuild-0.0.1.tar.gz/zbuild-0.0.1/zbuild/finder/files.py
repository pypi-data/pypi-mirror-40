#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os
import os.path
import re

from zbuild.log import logger

def get_files(filepath, fileext = r''):
    file_list = []
    if not os.path.exists(filepath):
        logger.info('Not exists path \"' + filepath + '\"')
        return file_list

    for root, dirs, filenames in os.walk(filepath):
        for filename in filenames:
            file_path = os.path.join(root, filename)
            if os.path.splitext(filename)[1] == fileext or fileext == '':
                file_list.append(os.path.abspath(file_path))

    return file_list