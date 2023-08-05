#!/usr/bin/env python

from setuptools import setup, find_packages

def readme():
    with open('README.adoc') as f:
        return f.read()

setup(
    name='vcdvcd',
    version='1.0.3',
    description='Python Verilog value change dump (VCD) parser library + the nifty vcdcat VCD command line viewer',
    long_description=readme(),
    url='https://github.com/cirosantilli/vcdvcd',
    author='Ciro Santilli',
    author_email='ciro.santilli.contact@gmail.com',
    packages=find_packages(),
    scripts=['vcdcat'],
)
