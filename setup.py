from distutils.core import setup
from Cython.Build import cythonize

setup(name="Cythonize4Connect",
    ext_modules=cythonize(["*.pyx", "screens/*.pyx"]),
)
