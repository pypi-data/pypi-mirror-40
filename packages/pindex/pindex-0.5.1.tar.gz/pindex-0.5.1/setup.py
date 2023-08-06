# -*- coding: utf-8 -*-

import codecs
import os
# import sys
 
#try:
from setuptools import setup
#except:
#    from distutils.core import setup

 
def read(fname):
    """
    define read method to read the long description.
    It will be shown in PyPI."""
    return codecs.open(os.path.join(os.path.dirname(__file__), fname)).read()
 
 
 
NAME = "pindex"

DESCRIPTION = "An awesome tool for indexing matrices. propose a new concept “single index” (as in matlab) to index the elements from matrices. exchange python-style index(begin with 0) with matlab-style index(begin with 1)"
 
LONG_DESCRIPTION = read("README.txt")
 
KEYWORDS = "Index, Matrix, Single Index, Style of Index"
 
AUTHOR = "William Song"
 
AUTHOR_EMAIL = "songcwzjut@163.com"
 
URL = "https://github.com/Freakwill/pindex"
 
VERSION = "0.5.1" # 修改版本号
 
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
