#!/usr/bin/env python

from os.path import exists
from setuptools import setup
import adispatch

setup(name='adispatch',
      version=adispatch.__version__,
      description='Multiple dispatch in function annotaions',
      url='http://github.com/waipu/adispatch/',
      author_email='waipu@cirno.de',
      license='BSD',
      keywords='dispatch',
      packages=['adispatch'],
      long_description=(open('README.rst').read() if exists('README.rst')
                        else ''),
      zip_safe=False)
