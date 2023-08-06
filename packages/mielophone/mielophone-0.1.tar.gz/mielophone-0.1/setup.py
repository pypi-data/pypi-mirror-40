#!/usr/bin/env python

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

with open("requirements.txt", "r") as fh:
    requires = [x.strip() for x in fh.readlines() if x]

import mielophone

setuptools.setup(
    name = "mielophone",
    version = mielophone.version,
    author = "Roman Kharin",
    author_email = "romiq.kh@gmail.com",
    description = "milo - Datum processing",
    long_description = long_description,
    long_description_content_type = "text/markdown",
    url = "https://github.com/RomanKharin/mielophone",
    packages = setuptools.find_packages(),
    requires = requires,
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
