# Copyright (c) 2011-2012 Ryan Bourgeois <bluedragonx@gmail.com>
#
# This project is free software according to the BSD-modified license. Refer to
# the LICENSE file for complete details.
"""
Test couchauth interfaces.
"""

import unittest
from pyramid_couchauth.interfaces import IIdentifier


class TestIIdentifier(unittest.TestCase):

    """Test the IIdentifier class."""

    def test_class(self):
        """Verify the class implements Interface."""
        self.assertTrue(hasattr(IIdentifier, 'names'),
            'class has no names attribute')
        self.assertTrue(hasattr(IIdentifier.names, '__call__'),
            'class names attribute is not callable')

    def test_names(self):
        """Verify the interface defines the correct methods."""
        names = set(['forget', 'identify', 'remember'])
        self.assertEqual(set(IIdentifier.names()), names,
            'class methods incorrect')

    def verify_method(self, method, params, kwargs):
        """Verify a method signature."""
        sig = IIdentifier.getDescriptionFor(method).getSignatureInfo()
        self.assertEqual(len(sig['positional']), params,
            'method %s contains invalid arguments' % method)
        self.assertEqual(sig['kwargs'] is not None, kwargs,
            'method %s contains invalid kwargs' % method)

    def test_identify(self):
        """Verify the method signature of identify."""
        self.verify_method('identify', 2, False)

    def test_remember(self):
        """Verify the method signature of remember."""
        self.verify_method('remember', 3, True)

    def test_forget(self):
        """Verify the method signature of forget."""
        self.verify_method('forget', 2, False)

