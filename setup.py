from distutils.core import setup
from Cython.Build import cythonize

setup(name="Cythonize4Connect",
    ext_modules=cythonize(["screens/minmax_ai.pyx", "screens/game.pyx", "screens/ai.pyx", "settings.pyx", "objects.pyx"]),
)
