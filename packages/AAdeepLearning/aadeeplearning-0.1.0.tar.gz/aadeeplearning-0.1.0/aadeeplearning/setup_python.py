from distutils.core import setup, Extension
import numpy


cos_doubles_module = Extension('_cos_doubles',
                           sources=['cos_doubles_wrap.cxx', 'cos_doubles.cpp'], )

setup (name = 'cos_doubles',
       version = '0.1',
       author      = "SWIG Docs",
       description = """Simple swig example from docs""",
       ext_modules = [cos_doubles_module],
       include_dirs = [numpy.get_include()],
       py_modules = ["cos_doubles"], )
