#!/usr/bin/env python

from distutils.core import setup

setup(
    name='gityamldb',
    version='0.3.0',
    description='Manage your data in Git versioned YAML files.',
    author='Ondrej Sika',
    author_email='ondrej@ondrejsika.com',
    url='https://github.com/gityamldb/gityamldb',
    packages=['gityamldb'],
    install_requires=[
        'gitpython',
        'pyaml',
    ],
    scripts=[
        'gyd-reformate',
        'gyd-validate',
    ],
)