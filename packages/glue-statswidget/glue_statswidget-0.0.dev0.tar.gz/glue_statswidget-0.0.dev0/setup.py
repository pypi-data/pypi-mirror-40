#!/usr/bin/env python
from __future__ import print_function
from setuptools import setup, find_packages

entry_points = """
[glue.plugins]
glue_statswidget=glue_statswidget:setup
"""

with open('README.rst') as infile:
    LONG_DESCRIPTION = infile.read()

with open('glue_statswidget/version.py') as infile:
    exec(infile.read())

setup(name='glue_statswidget',
      version=__version__,
      description='A Statistics Widget for Glue',
      long_description=LONG_DESCRIPTION,
      url="https://github.com/glue-viz/glue-plugin-template",
      author='Laura Chapman & Catherine Zucker',
      author_email='catherine.zucker@cfa.harvard.edu',
      packages = find_packages(),
      package_data={},
      entry_points=entry_points
    )
