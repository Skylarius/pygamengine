# -*- coding: utf-8 -*-

# Learn more: https://github.com/kennethreitz/setup.py

from setuptools import setup, find_packages

with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

# NB: requirements.txt and install_requires are not the same.
# Add here all required dependencies
requirements = [
    'nose',
    'pygame'
    ]

setup(
    name='pygamengine',
    version='0.1.0',
    description='Game Engine based on PyGame',
    long_description=readme,
    author='Ilario Gerloni',
    license=license,
    install_requires=requirements
    packages=find_packages(exclude=('tests', 'docs'))
)

