#!/usr/bin/env python
from setuptools import setup

setup(
    name="brainwallet",
    version="0.1",
    author="Warren MacEvoy",
    author_email="wmacevoy@gmail.com",
    description="Brain wallet tools",
    url="https://github.com/wmacevoy/brainwallet",
    packages=["brainwallet"],
    package_data={"brainwallet": ["wordlist/*.txt"]},
    zip_safe=False,
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: MacOS :: MacOS X",
    ],
)
