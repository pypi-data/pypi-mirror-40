#!/usr/bin/env python

from setuptools import setup

setup(
    name="list-github-repos",
    version="0.2",
    description="A utility that lists the repos from a GitHub profile",
    author="Kailash Nadh",
    author_email="kailash@nadh.in",
    url="https://github.com/knadh/list-github-repos",
    packages=["listgithubrepos"],
    download_url="https://github.com/knadh/list-github-repos",
    license="MIT License",
    entry_points={
        "console_scripts": [
            "list-github-repos = listgithubrepos.listgithubrepos:main",
        ],
    },
    classifiers=[
        "Topic :: Utilities",
        "Intended Audience :: Developers",
        "Programming Language :: Python",
        "Natural Language :: English",
        "License :: OSI Approved :: MIT License",
        "Topic :: Software Development :: Version Control :: Git",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
    ],
    install_requires=["bs4"]
)
