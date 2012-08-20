# Copyright (c) 2011-2012 Ryan Bourgeois <bluedragonx@gmail.com>
#
# This project is free software according to the BSD-modified license. Refer to
# the LICENSE file for complete details.
"""
Contains crypto related functions.
"""

import sys
import hashlib
import bcrypt
import base64
import random


__all__ = ['ShaHasher', 'BlowfishHasher', 'PasswordHasher']


class ShaHasher(object):

    """
    SHA-512 password hashing using hashlib.
    """

    def __init__(self):
        """Initialize the object."""

    def salt(self):
        """Generate a salt."""
        return ''.join([chr(random.choice(range(33, 127))) for n in range(32)])

    def encrypt(self, password, salt=None):
        """
        Hash a password using the optional salt. If the salt is not specified
        then one will be generated.

        :param password: The password to hash.
        :param salt: The salt to use when generating the hash.
        :return: The hashed password.
        """
        if salt is None:
            salt = self.salt()
        b64hash = base64.b64encode(hashlib.sha512(salt + password).digest())
        b64salt = base64.b64encode(salt)
        return '%s:%s' % (b64salt, b64hash)

    def compare(self, crypthash, password):
        """
        Compare a hashed password against a cleartext password.

        :param crypthash: The hashed password.
        :param password: The cleartext password.
        :return: True if they match, False if they don't.
        """
        hashparts = crypthash.split(':', 2)
        if len(hashparts) != 2:
            return False
        salt = base64.b64decode(hashparts[0])
        return self.encrypt(password, salt) == crypthash


class BlowfishHasher(object):

    """
    Blowfish password hashing using bcrypt.
    """

    def __init__(self, log_rounds=None):
        """Initialize the object."""
        self.log_rounds = log_rounds

    def salt(self):
        """Generate a salt."""
        return bcrypt.gensalt(self.log_rounds)

    def encrypt(self, password, salt=None):
        """
        Hash a password using the optional salt. If the salt is not specified
        then one will be generated.

        :param password: The password to hash.
        :param salt: The salt to use when generating the hash.
        :return: The hashed password.
        """
        if salt is None:
            salt = self.salt()
        return bcrypt.hashpw(password, salt)

    def compare(self, crypthash, password):
        """
        Compare a hashed password against a cleartext password.

        :param crypthash: The hashed password.
        :param password: The cleartext password.
        :return: True if they match, False if they don't.
        """
        return self.encrypt(password, crypthash) == crypthash


class PasswordHasher(object):

    """
    Password hashing facility.

    Hashes generated by this class have the algorithm prepended in {}'s and
    expected hashes passed to the compare method to be constructed the same
    way. If a hash was passed 
    """

    def __init__(self, algorithm='blowfish', **kwargs):
        """
        Initialize the password hasher.

        :param algorithm: The algorithm used to generate password hashes.
        :param kwargs: Arguments to pass to the __init__ of the underlying
            password hasher.
        """
        self.algorithm = algorithm
        self.hasher = self.find_hasher(algorithm, kwargs)
        if self.hasher is None:
            raise NotImplementedError('hashing algorithm %s is not implemented'
                % algorithm)

    def find_hasher(self, algorithm, kwargs=None):
        """
        Build a hasher that uses the given algorithm.

        :param algorithm: The algorithm to find a password hasher for.
        :param kwargs: Arguments to pass to the __init__ of the underlying
            password hasher.
        """
        if kwargs is None:
            kwargs = {}
        module = sys.modules[__name__]
        cls = '%sHasher' % algorithm.lower().title()
        if not hasattr(module, cls):
            return None
        classobj = getattr(module, cls)
        return classobj(**kwargs)

    def salt(self):
        """Generate a salt."""
        return self.hasher.salt()

    def encrypt(self, password, salt=None):
        """
        Hash a password using the optional salt. If the salt is not specified
        then one will be generated.

        :param password: The password to hash.
        :param salt: The salt to use when generating the hash.
        :return: The hashed password.
        """
        return '{%s}%s' % (self.algorithm, self.hasher.encrypt(password, salt))

    def compare(self, crypthash, password):
        """
        Compare a hashed password against a cleartext password. This method
        reads the determines the algorithm by reading the value inside of the
        {}'s at the beginning of the hash. If no algorithm is included with the
        hash then the algorithm given in __init__ is attempted. If no hasher is
        found for the given algorithm then False will immediately be returnd.

        :param crypthash: The hashed password.
        :param password: The cleartext password.
        :return: True if they match, False if they don't.
        """
        hasher = None
        algparts = crypthash.split('}', 2)
        if len(algparts) != 2:
            hasher = self.hasher
        else:
            crypthash = algparts[1]
            algorithm = algparts[0][1:]
            hasher = self.find_hasher(algorithm)
        if hasher is None:
            return False
        return hasher.compare(crypthash, password)

