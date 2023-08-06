import os
from cffi import FFI
ffi = FFI()
ffi.cdef("""
    int toto(int);
    int triple(int);
""")

C = ffi.dlopen(os.path.join(os.path.dirname(__file__), "rust_pypi.so"))

from .double import square, triple
from .version import __version__

__all__ = [
    'square',
    'triple',
]