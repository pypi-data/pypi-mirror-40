#!/usr/bin/env python

from setuptools import find_packages, setup

setup(
    name='grow-recipe',
    version='0.8.0',
    author='Jason Biegel',
    license='LICENSE',
    description='Store plant grow recipes in a structured XML format',
    package_data={'grow_recipe': ['grow-recipe.xsd']},
    packages=find_packages(exclude=['docs', 'samples', 'tests']),
    install_requires=[
        'lxml==4.1.1',
    ]
)
