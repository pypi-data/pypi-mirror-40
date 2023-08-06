# coding: utf-8

"""
    2z_team_nlp

    Utility package for Nexters 2Z team dev blogging project

"""


import sys
from setuptools import setup, find_packages
from os import path

NAME = "team_2z_nlp"
VERSION = "0.0.1"
# To install the library, run the following
#
# python setup.py install
#
# prerequisite: setuptools
# http://pypi.python.org/pypi/setuptoolss

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name=NAME,
    version=VERSION,
    description="",
    author_email="daesub0515@gmail.com",
    url="",
    keywords=["NEXTERS", "2Z", "konlpy", "nltk"],
    python_requires='>=3',
    packages=find_packages(),
    include_package_data=True,
    long_description="""\
    """
)
