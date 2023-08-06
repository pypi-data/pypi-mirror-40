# yall
Yet Another Lazy Loader for Python

    import yall
    yall.lazy_import('something') # instead of import something
    mod = yall.lazy_import('bbb.ccc') # instead of from bbb import ccc as mod

Based on internal importlib.util.LazyLoader and supports just Python 3.4 and newer.