#!/usr/bin/env python
# -*- coding: utf-8 -*-
import io
from setuptools import setup, find_packages


def read_file(filename):
    with io.open(filename) as fp:
        return fp.read().strip()


def read_requirements(filename):
    print filename
    return [line.strip() for line in read_file(filename).splitlines()
            if not line.startswith('#') and not line.startswith('--')]

setup(
    name='dcp-common',
    version=read_file('VERSION'),
    description="Common components for data collector platform.",
    long_description="Common components for data collector platform.",
    install_requires=read_requirements('requirements.txt'),
    packages=find_packages(),
    include_package_data=True,
    keywords=['scrapy-redis', 'simple'],
)
