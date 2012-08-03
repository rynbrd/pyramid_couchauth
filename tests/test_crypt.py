# Copyright (c) 2011-2012 Ryan Bourgeois <bluedragonx@gmail.com>
#
# This project is free software according to the BSD-modified license. Refer to
# the LICENSE file for complete details.
"""
Test the crypt module.
"""

import unittest
from pyramid_couchauth import crypt


class TestCrypt(unittest.TestCase):

    """
    Test the crypt module functions.
    """

    def setUp(self):
        """Set up test data."""
        self.salt = '$2a$12$.UDne5N2JYgWMGoY5Eu9G.'
        self.password = 'secret'
        self.pwhash = '$2a$12$.UDne5N2JYgWMGoY5Eu9G.71AI4v6oC/rQHkMFCIvXAMZgC9JtyB2'

    def test_hashpw(self):
        """Test the hashpw function."""
        pwhash = crypt.hashpw(self.password, self.salt)
        self.assertEqual(pwhash, self.pwhash,
            'failed to hash password')

    def test_hashcmp_true(self):
        """Test the hashcmp function when the password is valid."""
        self.assertTrue(crypt.hashcmp(self.pwhash, self.password),
            'hashcmp returned False with valid password')

    def test_hashcmp_false(self):
        """Test the hashcmp function when the password is invalid."""
        self.assertFalse(crypt.hashcmp(self.pwhash, 'badpass'),
            'hashcmp returned True with invalid password')

