#!/usr/bin/env python
import os.path
from setuptools import setup, find_packages


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name="async-json-rpc",
    version='0.0.0',
    packages=find_packages(),
    # metadata for upload to PyPI
    author="Kirill Pavlov",
    author_email="k@p99.io",
    url="https://github.com/pavlov99/async-json-rpc",
    description="Async JSON-RPC 2.0 server",
    long_description=read('README.rst'),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    license="MIT",
)
