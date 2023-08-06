#
# This file is part of yall (Yet Another Lazy Loader).
#

import sys
import importlib

def lazy_import(name, path=None):
    try:
        # todo: path is not supported here
        return sys.modules[name]
    except KeyError:
        spec = importlib.util.find_spec(name, path)
        loader = importlib.util.LazyLoader(spec.loader)

        module = importlib.util.module_from_spec(spec)
        loader.exec_module(module)
        return module
