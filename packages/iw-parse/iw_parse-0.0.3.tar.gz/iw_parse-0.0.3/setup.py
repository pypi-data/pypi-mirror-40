#! /usr/bin/env python

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="iw_parse",
    version="0.0.3",
    author="Brian Yahn",
    author_email="yahn007@outlook.com",
    description="A python parser for iwlist output",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/cuzzo/iw_parse",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
