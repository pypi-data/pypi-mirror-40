import os
from setuptools import setup

def _get_description():
    try:
        path = os.path.join(os.path.dirname(__file__), 'README.md')
        with open(path, encoding='utf-8') as f:
            return f.read()
    except IOError:
        return ''

setup(
    name='requests-paginator',
    version='0.2.0',
    author="chris48s",
    license="MIT",
    description='A generator for iterating over paginated API responses',
    long_description=_get_description(),
    long_description_content_type="text/markdown",
    url="https://github.com/chris48s/requests-paginator",
    packages=['requests_paginator'],
    install_requires=['requests'],
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
    ],
)
