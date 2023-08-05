#!/usr/bin/python
# -*- coding: UTF-8 -*-

from setuptools import setup, find_packages
import sys
import os
import os.path

try:
    import queue
except ImportError:
    import Queue as queue

__version__ = '0.0.1'

def get_data_files():
    datapath = os.getcwd() + '/'

    data_files = []
    dir_queue = queue.Queue()
    dir_queue.put(datapath + 'zbuild/data')
    while not dir_queue.empty():
        dir = dir_queue.get()
        for file_path in os.listdir(dir):
            file_path = os.path.join(dir, file_path)
            if os.path.isfile(file_path):
                file_path = file_path.replace(datapath, '')
                data_files.append(file_path)
            elif os.path.isdir(file_path):
                dir_queue.put(file_path)

    file_dirt = {str(): list()}
    for file_path in data_files:
        dirname = os.path.dirname(file_path).replace('\\', '/')
        if file_dirt.get(dirname, None) == None:
            file_dirt[dirname] = list()
        file_dirt[dirname].append(file_path)

    result = []
    for key, value in file_dirt.items():
        result.append((key, value))

    return result

setup(
    name = 'zbuild',
    version = __version__,
    description = 'Build myself sysytem.',
    author = 'Zeit',
    author_email='zeit.13@outlook.com',
    maintainer='Zeit',
    maintainer_email='zeit.13@outlook.com',
    url='https://pypi.org/',
    license="GPLv3",
    platforms=["any"],
    packages=[
        'zbuild',
        'zbuild/log',
        'zbuild/module',
        'zbuild/finder',
        'zbuild/generator',
        'zbuild/generator/project_files',
        'zbuild/generator/project_files/cmake'
    ],
    data_files=get_data_files(),
    # data_files=[
    #     ('data/cmake', ['data/cmake/common.cmake'])
    # ],
    package_data={
        'zbuild': ['zbuild/data/*']
    },
    classifiers=[
        'Programming Language :: Python :: 3.5',
        'Topic :: Scientific/Engineering :: Visualization'
    ],
    entry_points={'console_scripts': [
        'zbuild = zbuild.zbuild:main',
    ]},
    zip_safe=False,
    include_package_data=True
)
