#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

requirements = [
    "attrs >= 17.3",
    "functools32 >= 3.2.3; python_version<'3.0'",
    "singledispatch >= 3.4.0.3; python_version<'3.0'",
    "enum34 >= 1.1.6; python_version<'3.0'",
    "typing >= 3.5.3; python_version<'3.0'",
]


setup(
    name="jw-cattrs",
    version="1.0.1",
    description="Temporary cattrs fork",
    long_description="Temporary cattrs fork",
    author="John Walker",
    author_email="john@chaosdevs.com",
    url="https://github.com/j-walker23/cattrs",
    packages=find_packages(),
    include_package_data=True,
    install_requires=requirements,
    license="MIT license",
    zip_safe=False,
    keywords="cattrs",
    python_requires='~=3.7',
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3.7",
    ],
)
