#!/usr/bin/env python
# coding: utf-8

from setuptools import setup

setup(
    name='pytest-libfaketime',
    version='0.1.2',
    author='Éloi Rivard',
    author_email='eloi@yaal.fr',
    maintainer='The Yaal Team',
    maintainer_email='contact@yaal.fr',
    license='MIT',
    url='https://gitlab.com/yaal/pytest-libfaketime',
    description='A python-libfaketime plugin for pytest.',
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    py_modules=['pytest_libfaketime'],
    install_requires=[
        'libfaketime',
        'pytest>=3.0.0',
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Framework :: Pytest',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Testing',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: MIT License',
    ],
    entry_points={
        'pytest11': [
            'libfaketime = pytest_libfaketime',
        ],
    },
)
