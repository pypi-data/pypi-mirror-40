#!/usr/bin/python
# -*- coding: UTF-8 -*-

import importlib
import importlib.util
import importlib.machinery
import sys
sys.dont_write_bytecode = True

class _hacked_get_data:

    """Compatibility support for 'file' arguments of various load_*()
    functions."""

    def __init__(self, fullname, path, file=None):
        super().__init__(fullname, path)
        self.file = file

    def get_data(self, path):
        """Gross hack to contort loader to deal w/ load_*()'s bad API."""
        if self.file and path == self.path:
            # The contract of get_data() requires us to return bytes. Reopen the
            # file in binary mode if needed.
            if not self.file.closed:
                file = self.file
                if 'b' not in file.mode:
                    file.close()
            if self.file.closed:
                self.file = file = open(self.path, 'rb')

            with file:
                return file.read()
        else:
            return super().get_data(path)


class _load_source_compatibility(_hacked_get_data, importlib.machinery.SourceFileLoader):

    """Compatibility support for implementing load_source()."""

def load_source(name, pathname, file=None):
    loader = _load_source_compatibility(name, pathname, file)
    spec = importlib.util.spec_from_file_location(name, pathname, loader=loader)
    if name in sys.modules:
        module = importlib._bootstrap._exec(spec, sys.modules[name])
    else:
        module = importlib._bootstrap._load(spec)

    return module
