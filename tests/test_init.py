# Copyright (c) 2011-2012 Ryan Bourgeois <bluedragonx@gmail.com>
#
# This project is free software according to the BSD-modified license. Refer to
# the LICENSE file for complete details.
"""
Test the pyramid_couchauth module (__init__).
"""

import unittest
import pyramid_couchauth


class PackageTestData(unittest.TestCase):

    """
    Set up test data for the package.
    """

    def setUp(self):
        """Set up the test data."""
        self.db_key = 'couchauth.db'
        self.db_default = 'auth'
        self.db_custom = 'users'
        self.secret_key = 'couchauth.secret'
        self.secret_default = 'secret'
        self.secret_custom = 'EiT0phob'
        self.settings_default = {}
        self.settings_custom = {
            self.db_key: self.db_custom,
            self.secret_key: self.secret_custom}


class DummyConfig:

    """
    Dummy Pyramid config class.
    """

    def __init__(self, settings=None):
        """Initialize dummy config data."""
        if settings is None:
            settings = {}
        self.settings = settings
        self.authentication_policy = None
        self.authorization_policy = None

    def get_settings(self):
        """Get the settings object."""
        return self.settings

    def set_authentication_policy(self, policy):
        """Set the authentication policy."""
        self.authentication_policy = policy
        
    def set_authorization_policy(self, policy):
        """Set the authorization policy."""
        self.authorization_policy = policy


class TestSession(PackageTestData):

    """
    Test the Session class.
    """

    def test_class(self):
        """Test the class attributes."""
        self.assertEqual(pyramid_couchauth.Session.db_key, self.db_key,
            'db_key is invalid')
        self.assertEqual(pyramid_couchauth.Session.db_default, self.db_default,
            'db_default is invalid')
        self.assertEqual(pyramid_couchauth.Session.secret_key, self.secret_key,
            'secret_key is invalid')
        self.assertEqual(pyramid_couchauth.Session.secret_default,
            self.secret_default, 'secret_default is invalid')

    def test_init(self):
        """Test the __init__ method."""
        pyramid_couchauth.session = pyramid_couchauth.Session()
        self.assertFalse(pyramid_couchauth.session.configured,
            'session.configure is invalid')
        self.assertTrue(pyramid_couchauth.session.secret is None,
            'session.secret is invalid')
        self.assertTrue(pyramid_couchauth.session.dbname is None,
            'session.dbname is invalid')
        self.assertTrue(pyramid_couchauth.session._database is None,
            'session._database is invalid')

    def test_configure_present(self):
        """Test the configure method when settings are present."""
        pyramid_couchauth.session = pyramid_couchauth.Session()
        self.assertFalse(pyramid_couchauth.session.configured,
            'session.configured is invalid before configure')
        pyramid_couchauth.session.configure(self.settings_custom)
        self.assertEqual(pyramid_couchauth.session.dbname, self.db_custom,
            'session.dbname is invalid')
        self.assertEqual(pyramid_couchauth.session.secret, self.secret_custom,
            'session.secret is invalid')
        self.assertTrue(pyramid_couchauth.session._database is None,
            'session._database is invalid')
        self.assertTrue(pyramid_couchauth.session.configured,
            'session.configured is invalid after configure')

    def test_configure_absent(self):
        """Test the configure method when settings are absent."""
        pyramid_couchauth.session = pyramid_couchauth.Session()
        self.assertFalse(pyramid_couchauth.session.configured,
            'session.configured is invalid before configure')
        pyramid_couchauth.session.configure(self.settings_default)
        self.assertEqual(pyramid_couchauth.session.dbname, self.db_default,
            'session.dbname is invalid')
        self.assertEqual(pyramid_couchauth.session.secret, self.secret_default,
            'session.secret is invalid')
        self.assertTrue(pyramid_couchauth.session._database is None,
            'session._database is invalid')
        self.assertTrue(pyramid_couchauth.session.configured,
            'session.configured is invalid')
        self.assertTrue(pyramid_couchauth.session.configured,
            'session.configured is invalid after configure')

    def test_database(self):
        """Test the database property."""
        pyramid_couchauth.session.configure(self.settings_default)
        db = pyramid_couchauth.session.database
        self.assertEqual(db.dbname, self.db_default,
            'session.database is invalid')


class TestModuleFunctions(PackageTestData):

    """
    Test the module functions.
    """

    def test_configure_default(self):
        """Test the configure function."""
        """Test the configure function."""
        from pyramid_couchauth.policies import (CouchAuthenticationPolicy,
            CouchAuthorizationPolicy)

        config = DummyConfig(self.settings_default)
        pyramid_couchauth.session = pyramid_couchauth.Session()
        pyramid_couchauth.configure(config)

        self.assertIsInstance(config.authentication_policy,
            CouchAuthenticationPolicy,
            'authentication policy has invalid type')
        self.assertIsInstance(config.authorization_policy,
            CouchAuthorizationPolicy,
            'authorization policy has invalid type')

        self.assertEqual(config.authentication_policy.identifier.cookie.secret,
            self.secret_default, 'identifier secret is invalid')
        self.assertEqual(config.authentication_policy.database.dbname,
            self.db_default, 'authentication policy database is invalid')
        self.assertEqual(config.authorization_policy.database.dbname,
            self.db_default, 'authorization policy database is invalid')

    def test_configure_custom(self):
        """Test the configure function."""
        from pyramid_couchauth.policies import (CouchAuthenticationPolicy,
            CouchAuthorizationPolicy)

        config = DummyConfig(self.settings_default)
        pyramid_couchauth.session = pyramid_couchauth.Session()
        pyramid_couchauth.configure(config, self.secret_custom, self.db_custom)
        
        self.assertIsInstance(config.authentication_policy,
            CouchAuthenticationPolicy,
            'authentication policy has invalid type')
        self.assertIsInstance(config.authorization_policy,
            CouchAuthorizationPolicy,
            'authorization policy has invalid type')

        self.assertEqual(config.authentication_policy.identifier.cookie.secret,
            self.secret_custom, 'identifier secret is invalid')
        self.assertEqual(config.authentication_policy.database.dbname,
            self.db_custom, 'authentication policy database is invalid')
        self.assertEqual(config.authorization_policy.database.dbname,
            self.db_custom, 'authorization policy database is invalid')

