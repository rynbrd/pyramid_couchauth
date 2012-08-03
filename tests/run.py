# Copyright (c) 2011-2012 Ryan Bourgeois <bluedragonx@gmail.com>
#
# This project is free software according to the BSD-modified license. Refer to
# the LICENSE file for complete details.
"""
Execute tests.
"""

import unittest
import pyramid_couchauth.tests.test_principal
import pyramid_couchauth.tests.test_identification


def runtests():
    suites = unittest.TestSuite()
    suites.addTest(pyramid_couchauth.tests.test_principal.suite())
    suites.addTest(pyramid_couchauth.tests.test_identification.suite())
    return suites

