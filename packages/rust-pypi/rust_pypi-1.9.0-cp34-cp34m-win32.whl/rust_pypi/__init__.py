import os
import sys
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

    # For Linux and Darwin platforms, the generated lib file extension is .so
    dyn_lib_name = "rust_pypi*.so"

    if system == 'Windows':
        # On windows, it is a dll extension file
        dyn_lib_name = "rust_pypi*.dll"

    path = os.path.join(os.path.dirname(__file__), dyn_lib_name)
    filename = ""

    try:
        filename = glob(path)[0]
    except IndexError as e:
        print("Cannot find the dynamic lib located in: ", os.path.dirname(__file__))
        # Raising the exception to get the traceback
        raise

    return filename

dyn_lib_path = find_dynamic_lib_file()
C = ffi.dlopen(dyn_lib_path)

from .double import square, triple
from .version import __version__

__all__ = [
    'square',
    'triple',
]