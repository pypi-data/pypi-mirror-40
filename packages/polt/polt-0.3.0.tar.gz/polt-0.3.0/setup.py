#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# System modules
import os
import sys
import runpy
from setuptools import setup, find_packages


def read_file(filename):
    with open(filename, errors="ignore") as f:
        return f.read()


package = find_packages(exclude=["tests"])[0]

# run setup
setup(
    name=package,
    description="Live data visualisation via Matplotlib",
    author="Yann Büchau",
    author_email="nobodyinperson@gmx.de",
    keywords="live,plot,plotting,data,visualisation,matplotlib",
    license="GPLv3",
    version=runpy.run_path(os.path.join(package, "version.py")).get(
        "__version__", "0.0.0"
    ),
    url="https://gitlab.com/nobodyinperson/python3-polt",
    long_description=read_file("README.md"),
    long_description_content_type="text/markdown",
    classifiers=[
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)"
    ],
    install_requires=[
        "xdgspec>=0.1",
        "numpy>=1.15",
        "matplotlib>=3.0.2",
        "click>=7.0",
    ],
    tests_require=[],
    extras_require={},
    test_suite="tests",
    packages=find_packages(exclude=["tests"]),
    package_data={"polt.locale": ["*.mo"]},
    entry_points={"console_scripts": ["polt = polt.cli.commands.main:cli"]},
    include_package_data=True,
)
