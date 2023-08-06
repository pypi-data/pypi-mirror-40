#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pprint
import re
from setuptools import setup, find_packages

PACKAGE = 'metabeyond'
VERSION_PATTERN = re.compile(r'^__version__\s*=\s*[\"\'](.*?)[\"\']$', re.I | re.M | re.DOTALL)
AUTHOR_PATTERN = re.compile(r'^__author__\s*=\s*[\"\'](.*?)[\"\']$', re.I | re.M | re.DOTALL)
LICENSE_PATTERN = re.compile(r'^__licen[sc]e__\s*=\s*[\"\'](.*?)[\"\']$', re.I | re.M | re.DOTALL)
URL_PATTERN = re.compile(r'^__url__\s*=\s*[\"\'](.*?)[\"\']$', re.I | re.M | re.DOTALL)


def grep_first_match(file, regex, capture_group_range=0):
    with open(file) as fp:
        contents = fp.read()
    try:
        return regex.findall(contents)[capture_group_range]
    except IndexError:
        raise IndexError("Could not get result, maybe it couldn't be read?")


def parse_requirements(file):
    requirements = []
    with open(file) as fp:
        raw = fp.read()
        for line in raw.split('\n'):
            line = line.strip()
            if line and not line[0] == '#':
                requirements.append(line)
    return requirements


auto_attrs = dict(
    version=grep_first_match(PACKAGE + '/__init__.py', VERSION_PATTERN),
    author=grep_first_match(PACKAGE + '/__init__.py', AUTHOR_PATTERN),
    license=grep_first_match(PACKAGE + '/__init__.py', LICENSE_PATTERN),
    url=grep_first_match(PACKAGE + '/__init__.py', URL_PATTERN),
)

print('Resolved attributes:')
pprint.pprint(auto_attrs)


# Decent reference:
# https://gemfury.com/stevenferreira/python:sample/-/content/setup.py?gclid=Cj0KCQiApILhBRD1ARIsAOXWTztNWw_wmu2xA4Ka0yn-EjwbS99NZBI19Pjozfw7qAjVGSXDTY6grkkaAm1WEALw_wcB
setup(
    name=PACKAGE,
    description="Metadata for Python",
    long_description="Provides Java 6-like annotations, self-documenting decorators and additional type hinting "
                     "utilities to extend Python's typing module further.",
    # https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        # Development Status :: 1 - Planning
        # Development Status :: 2 - Pre-Alpha
        # Development Status :: 3 - Alpha
        # Development Status :: 4 - Beta
        # Development Status :: 5 - Production/Stable
        # Development Status :: 6 - Mature
        # Development Status :: 7 - Inactive
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Utilities',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    keywords='Metadata Java 6 annotation @interface hint documentation',
    packages=find_packages(exclude=['contrib', 'docs', 'tests*']),
    install_requires=parse_requirements('requirements.txt'),
    extras_require={
        'test': parse_requirements('test-requirements.txt'),
        'sast': parse_requirements('sast-requirements.txt'),
        'docs': parse_requirements('docs-requirements.txt'),
        'deploy': parse_requirements('deploy-requirements.txt'),
    },
    include_package_data=True,
    python_requires='>=3.6.0',
    **auto_attrs
)
