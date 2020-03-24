#!/usr/bin/env python

import imp
import sys

from setuptools import setup, find_packages

VERSION = imp.load_source("", "plotly_helper/version.py").__version__

setup(
    name="plotly-helper",
    author="Blue Brain Project, EPFL",
    version=VERSION,
    description="Package that makes plotly easy",
    url="https://github.com/bluebrain/plotly-helper",
    license="LGPLv3",
    install_requires=[
        'plotly>=3.4.2',
        'numpy>=1.15.4',
        'neurom>=1.4.13',
        'six>=1.12.0',
        'click>=6.0',
    ],
    entry_points={
        'console_scripts': ['viewer=plotly_helper.cli:cli']
    },
    packages=find_packages(),
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
    ],
)
