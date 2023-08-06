import os
from cffi import FFI

ffi = FFI()
ffi.cdef("""
    int toto(int);
    int triple(int);
""")

def find_dynamic_lib_file():
    from glob import glob
    import platform

    system = platform.system()

    if system == 'Windows':
        path = os.path.join(os.path.dirname(__file__), "rust_pypi*.dll")
    elif system == 'Darwin':
        path = os.path.join(os.path.dirname(__file__), "rust_pypi*.dylib")
    else:
        path = os.path.join(os.path.dirname(__file__), "rust_pypi*.so")

    filename = glob(path)[0]
    return filename

C = ffi.dlopen(find_dynamic_lib_file())

from .double import square, triple
from .version import __version__

__all__ = [
    'square',
    'triple',
]