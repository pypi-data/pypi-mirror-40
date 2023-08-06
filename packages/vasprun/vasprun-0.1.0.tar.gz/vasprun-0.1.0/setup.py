#!/usr/bin/env python3
#
# Copyright (C) 2018  Stanislav Markov
# Please see the accompanying LICENSE file for further information.

from setuptools import setup
import sys

if sys.version_info < (3, 0, 0, 'final', 0):
    raise SystemExit('Python 3 is required!')

setup(
    name="vasprun",
    version='0.1.0',
    description="Utility/library to process vasprun.xml, possibly more.",
    author="Stanislav Markov",
    url="https://github.com/smarkov/vasprun/",
    platforms="platform independent",
    package_dir={"": "src"},
    packages=[
        "vasprun",
    ],
    scripts=[
        "bin/vasprun",
    ],
    classifiers=[
        "Programming Language :: Python",
        "Environment :: Console",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering",
    ],
    long_description="""
Processing and converting data in vasprun.xml
-----------------------------------------------------------
A few routines and an executable to convert the XML file output by
the The Vienna Ab initio simulation package (VASP) to a json dictionary
with specific entries permitting analysis and plotting of density of
states (DoS) and band-structure.
""",
    install_requires = [
        "numpy",
        "ase",
        "lxml",
        "matplotlib",
        "json_tricks"
    ]
)
