# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

try:
    long_description = open("README.rst").read()
except IOError:
    long_description = ""

setup(
    name="python3-SmartSchema",
    version="1.1.0",
    description="Progressive update for schema",
    author="Jaiswal-ruhil",
    author_email="ruhiljaiswal@gmail.com",
    # scripts=['SmartSchema.py'],
    exclude=["*.tests", "*.tests.*", "tests.*", "tests", "test"],
    packages=find_packages(),
    long_description=long_description,
    license="MIT",
    url="https://pypi.org/project/python3-SmartSchema/",
    classifiers=[
        "Programming Language :: Python :: 3.6",
    ],
    install_requires=[
        'jsonschema>=2.6.0'
    ]
)
