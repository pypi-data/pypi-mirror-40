from cffi import FFI
ffi = FFI()
ffi.cdef("""
    int toto(int);
    int triple(int);
""")

C = ffi.dlopen("../rust-pypi/target/debug/librust_pypi.so")

from .double import square, triple

__all__ = [
    'square',
    'triple',
]