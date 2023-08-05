# -*- coding: utf-8 -*-

# Learn more: https://github.com/kennethreitz/setup.py

from setuptools import setup, find_packages


with open('README.txt') as f:
    readme = f.read()

setup(
    name='prettydataloader',
    version='0.1.1',
    description='Pretty Data Loader',
    long_description=readme,
    author='Atsushi Nakajima',
    author_email='summer4an@gmail.com',
    url='https://github.com/summer4an',
    license='MIT',
    packages=find_packages(exclude=('temporal*', 'test*', 'tests', 'docs'))
)

