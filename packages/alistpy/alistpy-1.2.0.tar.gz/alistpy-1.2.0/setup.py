#!/usr/bin/env python

import setuptools
from distutils.core import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name='alistpy',
      version='1.2.0',
      description='An Association List construct',
      long_description = long_description,
      long_description_content_type="text/markdown",
      author='James Milne',
      author_email='james.milne@protonmail.com',
      url='https://git.sr.ht/~shakna/alistpy',
      py_modules=['alist'],
      packages=setuptools.find_packages(),
      classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
     ],
     )
