#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name='singer-target-postgres',
    version="0.1.0",
    description='Singer.io target for loading data into postgres',
    classifiers=['Programming Language :: Python :: 3 :: Only'],
    py_modules=['target_postgres'],
    install_requires=[
        'arrow==0.12.1',
        'jsonschema==2.6.0',
        'psycopg2==2.7.4',
        'psycopg2-binary==2.7.4',
        'singer-python==5.0.12'
    ],
    setup_requires=[
        "pytest-runner"
    ],
    tests_require=[
        "chance==0.110",
        "Faker==0.9.2",
        "pytest==3.9.3"
    ],
    entry_points='''
      [console_scripts]
      target-postgres=target_postgres:cli
    ''',
    packages=find_packages()
)
