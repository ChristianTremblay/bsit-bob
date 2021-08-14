#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# python setup.py install


import os
import sys
import re

from setuptools import setup, find_packages

# load in the project metadata
init_py = open(os.path.join("bob", "__init__.py")).read()
metadata = dict(re.findall("""__([a-z]+)__ = ["]([^"]+)["]""", init_py))

requirements = [
    "rdflib",
]

setup(
    name="bob",
    version=metadata["version"],
    description="Bob the SI-WG Builder",
    long_description="Tool for building RDF graphs of HVAC systems",
    author=metadata["author"],
    author_email=metadata["email"],
    packages=find_packages(),
    install_requires=requirements,
    license="MIT",
    zip_safe=False,
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
)
