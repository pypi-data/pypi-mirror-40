def square(x):
    from cffi import FFI
    ffi = FFI()
    ffi.cdef("""
        int double(int);
    """)

    C = ffi.dlopen("../rust-pypi/target/debug/librust_pypi.so")

    print(C.double(9))