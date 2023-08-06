#!/usr/bin/env python3

"""
Blizzard API CLI - Package distribution.

Vaughn Kottler 01/07/19
"""

# third-party
from setuptools import setup, find_packages

# internal
from blizzard_api import VERSION, DESCRIPTION

# https://packaging.python.org/tutorials/packaging-projects/
with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name="blizzard_api",
      version=VERSION,
      packages=find_packages(),
      install_requires=["requests"],
      package_data={"": ["*.json"]},
      author="Vaughn Kottler",
      author_email="vaughnkottler@gmail.com",
      description=DESCRIPTION,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/vkottler/blizzard-api-cli",
      classifiers=["Programming Language :: Python :: 3.5",
                   "License :: OSI Approved :: MIT License",
                   "Operating System :: Unix"],
      entry_points={"console_scripts": ["bapi = blizzard_api.client:main"]})
