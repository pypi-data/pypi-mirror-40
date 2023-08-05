# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

try:
    long_description = open("README.rst").read()
except IOError:
    long_description = ""

setup(
    name="python3-SmartSchema",
    version="0.1.3",
    description="Progressive update for schema",
    author="Jaiswal-ruhil",
    author_email="cschultz@example.com",
    scripts=['SmartSchema.py'],
    exclude=["*.tests", "*.tests.*", "tests.*", "tests", "test"],
    packages=find_packages(),
    long_description=long_description,
    classifiers=[
        "Programming Language :: Python :: 3.6",
    ]
)
