#!/usr/bin/env python3
 
from setuptools import setup
import pathlib
 

NAME = "fcool"

DESCRIPTION = "A cool tool for functional programming. Funtions can be operated directly with definition domain that can be used in type testing"
 
LONG_DESCRIPTION = pathlib.Path("README.txt").read_text()
 
KEYWORDS = "Functional Programming, Type Testing"
 
AUTHOR = "William Song"
 
AUTHOR_EMAIL = "songcwzjut@163.com"
 
URL = "https://github.com/Freakwill/fcool"
 
VERSION = "0.1.3" # update the version before uploading
 
LICENSE = "MIT"

 
setup(
    name = NAME,
    py_modules = [NAME],
    version = VERSION,
    description = DESCRIPTION,
    long_description = LONG_DESCRIPTION,
    classifiers = [
        'License :: Public Domain',  # Public Domain
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Intended Audience :: Science/Research',
        'Operating System :: OS Independent',
        'Topic :: Scientific/Engineering :: Mathematics',
        'Natural Language :: English'
    ],
    keywords = KEYWORDS,
    author = AUTHOR,
    author_email = AUTHOR_EMAIL,
    url = URL,
    license = LICENSE,
    # packages = PACKAGES,
    include_package_data=True,
    zip_safe=True,
)
