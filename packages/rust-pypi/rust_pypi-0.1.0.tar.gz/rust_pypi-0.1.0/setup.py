#!/usr/bin/env python

from setuptools import setup, find_packages

setup(name='rust_pypi',
    packages=find_packages(),
    version="0.1.0",
    description='Rust pypi',
    author='Thomas Boch, Matthieu Baumann',
    author_email='matthieu.baumann@astro.unistra.fr',
    license='BSD',
    provides=['rust_pypi'],
)
