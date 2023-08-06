#!/usr/bin/env python

from distutils.core import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name='blockchair',
      version='1.0.2',
      description='Blockchair API Python Library',
      author='Rustam Sultanov',
      author_email='info@blockchair.com',
      url='https://golf.blockchair.com/RustamSultanov/blockchair-python-sdk',
      license='MIT',
      packages=['blockchair'],
      keywords='blockchair.com api explorer',
      classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: Financial and Insurance Industry",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.0",
        "Programming Language :: Python :: 3.1",
        "Programming Language :: Python :: 3.2",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Topic :: Office/Business :: Financial",
        "License :: OSI Approved :: MIT License",
        ],
)
