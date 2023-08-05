#!/usr/bin/env python3
from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name='netorcai',
      version='1.0.0',
      description='Python version of the netorcai client library',
      long_description=long_description,
      author='Millian Poquet',
      author_email='millian.poquet@gmail.com',
      url='https://github.com/netorcai/netorcai-client-python/',
      packages=['netorcai'],
      license='LGPLv3',
      classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)",
        "Operating System :: OS Independent",
    ],
 )
