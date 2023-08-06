#!/usr/bin/env python

from os.path import exists
from setuptools import setup
import pybimaps

setup(name='pybimaps',
      version=pybimaps.__version__,
      description='Various bijective maps in pure python.',
      url='https://github.com/waipu/pybimaps',
      author='waipu',
      author_email='waipu@cirno.de',
      license='GPL3',
      keywords='bijective map',
      packages=['pybimaps'],
      long_description=(open('README.rst').read() if exists('README.rst')
                        else ''),
      zip_safe=False)
