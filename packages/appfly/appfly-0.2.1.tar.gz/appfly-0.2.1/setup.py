#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages
from appfly import __version__ as version

with open('README.md') as readme_file:
    readme = readme_file.read()

with open('HISTORY.md') as history_file:
    history = history_file.read()

requirements = [
    'Flask==1.0.2',
    'flask_cors==3.0.6', 
    'Flask-SocketIO==3.0.2',
    'jsonmerge==1.5.2'
]

setup(
    author="Italo José G. de Oliveira",
    author_email='italo.i@live.com',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    description="This pkg encapsulate the base flask server configurations",
    install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='appfly',
    name='appfly',
    packages=find_packages(),
    url='https://github.com/italojs/appfly',
    version=version,
    zip_safe=False,
)
