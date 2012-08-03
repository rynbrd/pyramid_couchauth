# Copyright (c) 2011-2012 Ryan Bourgeois <bluedragonx@gmail.com>
#
# This project is free software according to the BSD-modified license. Refer to
# the LICENSE file for complete details.
"""
Test the crypt module.
"""

import unittest
from pyramid_couchauth.crypt import ShaHasher, BlowfishHasher, PasswordHasher


class TestShaHasher(unittest.TestCase):

    """
    Test the SHA-512 hasher.
    """

    def setUp(self):
        """Set up test data."""
        self.salt = 'g_cPlUnc29O1Ua/`$5R\'x91ls1"R4&h6'
        self.password = 'secret'
        self.pwhash = ('Z19jUGxVbmMyOU8xVWEvYCQ1Uid4OTFsczEiUjQmaDY=:' +
            'qgN64+wpWGA90TE/hcndasfNAyepwMALtp65RQ5vVuKZU+zGwDWj1/1fO' +
            'GvZ7YXOUrD40tNXxqxDXEbavk++mQ==')
        self.hasher = ShaHasher()

    def test_encrypt(self):
        """Test the encrypt method."""
        pwhash = self.hasher.encrypt(self.password, self.salt)
        self.assertEqual(pwhash, self.pwhash,
            'failed to encrypt password')

    def test_salt(self):
        """Test the salt method."""
        self.assertTrue(len(self.hasher.salt()) > 0,
            'no salt generated')
        self.assertNotEqual(self.hasher.salt(), self.hasher.salt(),
            'generated salts are identical')

    def test_compare_true(self):
        """Test the compare method when the password is valid."""
        self.assertTrue(self.hasher.compare(self.pwhash, self.password),
            'returned False with valid password')

    def test_compare_false(self):
        """Test the compare method when the password is invalid."""
        self.assertFalse(self.hasher.compare(self.pwhash, 'badpass'),
            'returned True with invalid password')


class TestBlowfishHasher(unittest.TestCase):

    """
    Test the Blowfish hasher.
    """

    def setUp(self):
        """Set up test data."""
        self.salt = '$2a$12$.UDne5N2JYgWMGoY5Eu9G.'
        self.password = 'secret'
        self.pwhash = '$2a$12$.UDne5N2JYgWMGoY5Eu9G.71AI4v6oC/rQHkMFCIvXAMZgC9JtyB2'
        self.log_rounds = 12
        self.hasher = BlowfishHasher(self.log_rounds)

    def test_init(self):
        """Test the __init__ methdod."""
        self.assertEqual(self.hasher.log_rounds, self.log_rounds,
            'log_rounds not set to parameter value')

    def test_salt(self):
        """Test the salt method."""
        self.assertTrue(len(self.hasher.salt()) > 0,
            'no salt generated')
        self.assertNotEqual(self.hasher.salt(), self.hasher.salt(),
            'generated salts are identical')

    def test_encrypt(self):
        """Test the encrypt method."""
        pwhash = self.hasher.encrypt(self.password, self.salt)
        self.assertEqual(pwhash, self.pwhash,
            'failed to encrypt password')

    def test_compare_true(self):
        """Test the compare method when the password is valid."""
        self.assertTrue(self.hasher.compare(self.pwhash, self.password),
            'returned False with valid password')

    def test_compare_false(self):
        """Test the compare method when the password is invalid."""
        self.assertFalse(self.hasher.compare(self.pwhash, 'badpass'),
            'returned True with invalid password')


class TestPasswordHasher(unittest.TestCase):

    """
    Test the password hasher.
    """

    def setUp(self):
        """Set up test data."""
        self.algorithm = 'blowfish'
        self.salt = '$2a$12$.UDne5N2JYgWMGoY5Eu9G.'
        self.password = 'secret'
        self.bfhash = ('$2a$12$.UDne5N2JYgWMGoY5Eu9G.71AI4v6oC' +
            '/rQHkMFCIvXAMZgC9JtyB2')
        self.shahash = '$2a$12$.UDne5N2JYgWMGoY5Eu9G.71AI4v6oC/rQHkMFCIvXAMZgC9JtyB2'
        self.log_rounds = 10
        self.hasher = PasswordHasher(log_rounds=self.log_rounds)

    def test_init(self):
        """Test the __init__ method."""
        self.assertEqual(self.hasher.algorithm, 'blowfish',
            'algorithm is not set to default')
        self.assertEqual(self.hasher.hasher.log_rounds, self.log_rounds,
            'parameters not passed to underlying hasher')

    def test_init_badalg(self):
        """Test the __init__ method with an invalid algorithm."""
        with self.assertRaises(NotImplementedError):
            PasswordHasher('badalg')

    def test_find_hasher(self):
        """Test the find_hasher method."""
        algorithm = 'sha'
        self.assertTrue(self.hasher.find_hasher('sha') is not None,
            'no hasher found')

    def test_salt(self):
        """Test the salt method."""
        self.assertTrue(len(self.hasher.salt()) > 0,
            'no salt generated')
        self.assertNotEqual(self.hasher.salt(), self.hasher.salt(),
            'generated salts are identical')

    def test_encrypt(self):
        """Test the encrypt method."""
        pwhash = self.hasher.encrypt(self.password, self.salt)
        bfhash = '{%s}%s' % (self.algorithm, self.bfhash)
        self.assertEqual(pwhash, bfhash,
            'failed to encrypt password')

    def test_compare_true(self):
        """Test the compare method when the password is valid."""
        pwhash = '{%s}%s' % (self.algorithm, self.bfhash)
        self.assertTrue(self.hasher.compare(pwhash, self.password),
            'returned False with valid password')

    def test_compare_false(self):
        """Test the compare method when the password is invalid."""
        pwhash = '{%s}%s' % (self.algorithm, self.bfhash)
        self.assertFalse(self.hasher.compare(pwhash, 'badpass'),
            'returned True with invalid password')

    def test_compare_true_noalg(self):
        """
        Test the compare method with a valid password when no algorithm is
        present.
        """
        self.assertTrue(self.hasher.compare(self.bfhash, self.password),
            'returned False with valid password')

    def test_compare_false_noalg(self):
        """
        Test the compare method with an invalid password when no algorithm is
        present.
        """
        self.assertFalse(self.hasher.compare(self.bfhash, 'badpass'),
            'returned True with invalid password')

    def test_compare_true_altalg(self):
        """
        Test the compare method with a valid password when the algorithm
        differs.
        """
        self.assertTrue(self.hasher.compare(self.shahash, self.password),
            'returned False with valid password')

    def test_compare_false_noalg(self):
        """
        Test the compare method with an invalid password when the algorithm
        differs.
        """
        self.assertFalse(self.hasher.compare(self.shahash, 'badpass'),
            'returned True with invalid password')

