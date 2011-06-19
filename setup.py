# Copyright (c) 2011, Ryan Bourgeois <bluedragonx@gmail.com>
# All rights reserved.
#
# This software is licensed under a modified BSD license as defined in the
# provided license file at the root of this project.  You may modify and/or
# distribute in accordance with those terms.
#
# This software is provided "as is" and any express or implied warranties,
# including, but not limited to, the implied warranties of merchantability and
# fitness for a particular purpose are disclaimed.

from setuptools import setup, find_packages
import sys, os

version = '0.1alpha1'

setup(name = 'pyramid_couchauth',
    version = version,
    description = "Pyramid CouchDB Auth Add-On",
    long_description = "Pyramid add-on to provide authentication and authorization against CouchDB.",
    classifiers = [], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
    keywords = '',
    author = 'Ryan Bourgeois',
    author_email = 'bluedragonx@gmail.com',
    url = 'https://github.com/BlueDragonX/pyramid_couchauth',
    license = 'BSD-derived',
    packages = find_packages(exclude=['ez_setup', 'examples', 'tests']),
    include_package_data = True,
    zip_safe = False,
    install_requires = [
        'pyramid >= 1.0',
        'couchdbkit >= 0.5.0'],
    entry_points = "")
