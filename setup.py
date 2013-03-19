#!/bin/env python
# -*- coding:utf-8 -*-

from distribute_setup import use_setuptools
use_setuptools()

from setuptools import setup, find_packages

version = "0.1.0"

setup(
    name="",
    version=version,
    description="A command-line way to view PEPs while working in a terminal on- or off-line.",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Environment :: Console :: Curses",
        "Operating System :: Unix",
        "License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)"
    ],
    keywords="pep",
    author="Ryan Brown",
    author_email="ryansb@csh.rit.edu",
    url="http://github.com/ryansb/pepbrowser",
    license="GPL",
    packages=find_packages(
    ),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        "urwid"
    ]
    #TODO: Deal with entry_points
    #entry_points="""
    #[console_scripts]
    #pythong = pythong.util:parse_args
    #"""
)
