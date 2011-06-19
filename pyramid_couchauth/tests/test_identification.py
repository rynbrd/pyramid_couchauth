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

import unittest
from pyramid_couchauth.interfaces import IIdentifier
from pyramid_couchauth.identification import AuthTktIdentifier

def suite():
    return unittest.defaultTestLoader.loadTestsFromTestCase(TestAuthTktIdentifier)

class TestAuthTktIdentifier(unittest.TestCase):

    def test_interface(self):
        self.assertTrue(IIdentifier.implementedBy(AuthTktIdentifier))

