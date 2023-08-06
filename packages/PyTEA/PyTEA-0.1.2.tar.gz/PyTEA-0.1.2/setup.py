# -*- coding: utf-8 -*-
from setuptools import find_packages, setup

with open('README.rst') as f:
    readme = f.read()


setup(
    name='PyTEA',
    version='0.1.2',
    description='Tiny Encryption Algorithm (TEA) in Python.',
    long_description=readme,
    author='codeif',
    author_email='me@codeif.com',
    url='https://github.com/codeif/PyTEA',
    license='MIT',
    packages=find_packages(),
)
