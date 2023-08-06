def init_libpython():
    import ctypes
    import pkg_resources
    t = pkg_resources.resource_filename(__name__, "libpython2.7.so.1.0")
    ctypes.CDLL(t)
