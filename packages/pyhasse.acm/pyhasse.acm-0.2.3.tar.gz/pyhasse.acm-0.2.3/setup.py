#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requires = [
    'setuptools',
    'pyhasse.core'
]


setup_requirements = ['pytest-runner', ]
test_requirements = ['pytest', ]

setup(
    author="Rainer Bruggemann",
    author_email='rainer.bruggemann@pyhasse.org',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.7',
    ],
    description="PyHasse module: pyhasse.acm",
    install_requires=requires,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='acm',
    packages=['pyhasse.acm'],
    namespace_packages=['pyhasse'],
    name='pyhasse.acm',
    package_dir={'': 'src'},
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://pyhasse.org',
    version='0.2.3',
    zip_safe=False,
)
