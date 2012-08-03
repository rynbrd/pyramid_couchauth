# Copyright (c) 2011-2012 Ryan Bourgeois <bluedragonx@gmail.com>
#
# This project is free software according to the BSD-modified license. Refer to
# the LICENSE file for complete details.
"""
Package implementing auth/auth support in Pyramid against CouchDB.
"""

import os
import sys
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
readme = os.path.join(here, 'README.md')

requires = [
    'pyramid>=1.0',
    'couchdbkit>=0.5.0']
testing_extras = [
    'nose']

setup(
    name='pyramid_couchauth',
    version='0.1',
    description='CouchDB auth/auth support for Pyramid.',
    long_description=open(readme).read(),
    classifiers=[
        "Intended Audience :: Developers",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Framework :: Pyramid",
        "License :: OSI Approved :: BSD License"],
    keywords='web wsgi pylons pyramid couchdb',
    author='Ryan Bourgeois',
    author_email='bluedragonx@gmail.com',
    url='https://github.com/BlueDragonX/pyramid_couchauth',
    license='BSD-derived',
    zip_safe=False,
    packages=find_packages(exclude=['tests']),
    include_package_data=True,
    install_requires=requires,
    tests_require=requires + testing_extras,
    entry_points="")

