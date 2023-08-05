#!/usr/bin/env python
import platform
import sys
from glob import glob
import json

try:
    # Use setuptools if available, for install_requires (among other things).
    import setuptools
    from setuptools import setup, Extension
except ImportError:
    setuptools = None
    from distutils.core import setup, Extension

# Classic setup.py

kwargs = {}

# Version configuration
with open('rook/rookout-config.json', 'r') as f:
    config = json.load(f)
version = config['VersionConfiguration']['VERSION']

# Readme
with open('README.rst') as f:
    kwargs['long_description'] = f.read()

if sys.platform in ('darwin', 'linux2', 'linux'):
    ext_modules = []
    extra_compile_args = [
        '-std=c++0x',
        '-g0',
        '-O3',
        '-Wno-deprecated-register']

    if sys.platform == 'darwin':
        extra_compile_args.append("-mmacosx-version-min=" + platform.mac_ver()[0])

    if ('CPython' == platform.python_implementation()) and \
            ((sys.version_info[0] == 2 and sys.version_info > (2, 7, 0)) or
             (sys.version_info[0] == 3 and sys.version_info >= (3, 5, 0))):
        ext_modules.append(Extension(
            'rook.services.cdbg_native',
            sources=glob('rook/services/exts/cloud_debug_python/*.cc'),
            extra_compile_args=extra_compile_args))

    ext_modules.append(Extension(
        'native_extensions',
        sources=glob('rook/native_extensions/*.cc'),
        extra_compile_args=extra_compile_args))

    kwargs['ext_modules'] = ext_modules


if setuptools is not None:
    # If setuptools is not available, you're on your own for dependencies.
    install_requires = [
        "six >= 1.11",
        "grpcio >= 1.14.1",
        "protobuf >= 3.5.0, <= 4.0.0",
        "pyparsing"
    ]

    kwargs['install_requires'] = install_requires

setup(
    name="rook",
    version=version,
    packages=setuptools.find_packages(where='.', exclude=['contrib', 'docs', '*test*']),
    include_package_data=True,
    author="Rookout",
    author_email="liran@rookout.com",
    url="http://rookout.com/",
    description="Rook is a Python package for on the fly debugging and data extraction for application in production",
    license="https://get.rookout.com/SDK_LICENSE.pdf",
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',

        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: Implementation :: CPython',

        ],
    zip_safe=False,
    **kwargs
)
