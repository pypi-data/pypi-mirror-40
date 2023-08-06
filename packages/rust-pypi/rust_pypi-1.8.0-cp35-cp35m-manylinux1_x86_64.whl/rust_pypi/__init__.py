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

    dyn_lib_name = "rust_pypi*.so"

    if system == 'Windows':
        dyn_lib_name = "rust_pypi*.dll"
    elif system == 'Darwin':
        dyn_lib_name = "rust_pypi*.dylib"

    try:
        path = os.path.join(os.path.dirname(__file__), dyn_lib_name)
        filename = glob(path)[0]
    except IndexError as e:
        print(e)
        print("Cannot find the dynamic lib located at: ", path)

    return filename

C = ffi.dlopen(find_dynamic_lib_file())

from .double import square, triple
from .version import __version__

__all__ = [
    'square',
    'triple',
]