#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Sparse matrix operations
"""

import sys

import setuptools
from setuptools import setup, find_packages, Extension
from setuptools.command.build_ext import build_ext

import os

#os.environ["CC"] = "/usr/local/bin/gcc-8"
#os.environ["CXX"] = "/usr/local/bin/g++-8"
os.environ["CC"] = "/usr/local/opt/llvm/bin/clang"
os.environ["CXX"] = "/usr/local/opt/llvm/bin/clang++"

install_requires = (
    'omp_thread_count',
    'scipy',
    'tqdm',
    'pybind11>=2.2'
)

# As of Python 3.6, CCompiler has a `has_flag` method.
# cf http://bugs.python.org/issue26689
def has_flag(compiler, flagname):
    """Return a boolean indicating whether a flag name is supported on
    the specified compiler.
    """
    import tempfile
    with tempfile.NamedTemporaryFile('w', suffix='.cpp') as f:
        f.write('int main (int argc, char **argv) { return 0; }')
        try:
            compiler.compile([f.name], extra_postargs=[flagname])
        except setuptools.distutils.errors.CompileError:
            return False
    return True


def cpp_flag(compiler):
    """Return the -std=c++[11/14] compiler flag.

    The c++14 is prefered over c++11 (when it is available).
    """
    if has_flag(compiler, '-std=c++14'):
        return '-std=c++14'
    elif has_flag(compiler, '-std=c++11'):
        return '-std=c++11'
    else:
        raise RuntimeError('Unsupported compiler -- at least C++11 support '
                           'is needed!')

def omp_flag(compiler):
    """Return the -fopenmp flag
    """
    fopenmp = '-fopenmp'
    if has_flag(compiler, fopenmp):
        return fopenmp
    else:
        raise RuntimeError('Unsupported compiler -- OpenMP is needed')


class BuildExt(build_ext):
    """A custom build extension for adding compiler-specific options."""
    c_opts = {
        'msvc': ['/EHsc'],
        'unix': [],
    }

    if sys.platform == 'darwin':
        #c_opts['unix'] += ['-stdlib=libc++', '-mmacosx-version-min=10.7']
        pass

    def build_extensions(self):
        self.compiler.compiler_so.remove('-Wstrict-prototypes')
        ct = self.compiler.compiler_type
        opts = self.c_opts.get(ct, [])
        if ct == 'unix':
            opts.append('-DVERSION_INFO="%s"' % self.distribution.get_version())
            opts.append(cpp_flag(self.compiler))
            opts.append(omp_flag(self.compiler))
            if has_flag(self.compiler, '-fvisibility=hidden'):
                opts.append('-fvisibility=hidden')
        elif ct == 'msvc':
            opts.append('/DVERSION_INFO=\\"%s\\"' % self.distribution.get_version())
        for ext in self.extensions:
            ext.extra_compile_args = opts
        build_ext.build_extensions(self)


class get_pybind_include(object):
    """Helper class to determine the pybind11 include path

    The purpose of this class is to postpone importing pybind11
    until it is actually installed, so that the ``get_include()``
    method can be invoked. """

    def __init__(self, user=False):
        self.user = user

    def __str__(self):
        import pybind11
        return pybind11.get_include(self.user)


ext_modules = [
    Extension(
        'sparse',
        sources=['sparse_bind.cpp'],
        include_dirs=[
            # Path to pybind11 headers
            get_pybind_include(),
            get_pybind_include(user=True)
        ],
        language='c++'
    ),
]

setup(
    name='sparse-opts',
    version='0.1.0',
    author='Luke Olson',
    author_email='luke.olson@gmail.com',
    maintainer='Luke Olson',
    maintainer_email='luke.olson@gmail.com',
    license='MIT',
    platforms=['Windows', 'Linux', 'Mac OS-X', 'Unix'],
    description=__doc__.split('\n')[0],
    long_description=__doc__,
    #
    packages=find_packages(),
    install_requires=install_requires,
    #
    ext_modules=ext_modules,
    cmdclass={'build_ext': BuildExt},
    setup_requires=['pybind11'],
)
