#!/usr/bin/python
# -*- coding: UTF-8 -*-

# global values
# values = {}


global _global_dict
_global_dict = {}

def set(name, value):
    _global_dict[name] = value

def get(name, defValue=None):
    try:
        return _global_dict[name]
    except KeyError:
        return defValue