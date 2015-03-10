import os
from setuptools import setup

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.rst'), encoding = 'utf-8') as f:
    long_desc = f.read()

setup(
    name = "python-cloudatcost",
    version = "0.5",
    author = "Andy Culler",
    author_email = "adc4392@gmail.com",
    description = ("A python wrapper for the cloudatcost.com API - "
                   "https://github.com/cloudatcost/api"),
    license = "MIT",
    keywords = "wrapper for cloud at cost api",
    url = "https://github.com/adc4392/python-cloudatcost",
    packages = ['cacpy'],
    long_description = long_desc,
    classifiers = [
        "Indented Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: Python :: 2.7",
        "License :: OSI Approved :: MIT License",
    ],
    install_requires = ['requests']
)
