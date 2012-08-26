# Copyright (c) 2011-2012 Ryan Bourgeois <bluedragonx@gmail.com>
#
# This project is free software according to the BSD-modified license. Refer to
# the LICENSE file for complete details.
"""
Test the pyramid_couchauth module.
"""

import unittest
import pyramid_couchdb
import pyramid_couchauth
from pyramid_couchauth import Session
from pyramid_couchauth.policies import (CouchAuthenticationPolicy,
    CouchAuthorizationPolicy)


class DummyConfig(object):

    """
    Dummy Pyramid config class.
    """

    def __init__(self, settings):
        """Initialize dummy config data."""
        self.settings = settings
        self.authentication_policy = None
        self.authorization_policy = None

    def get_settings(self):
        """Get the settings object."""
        return self.settings

    def add_subscriber(self, handler, eventtype):
        """Pretend to add an event subscriber to the dummy."""

    def set_authentication_policy(self, policy):
        """Set the authentication policy."""
        self.authentication_policy = policy

    def set_authorization_policy(self, policy):
        """Set the authorization policy."""
        self.authorization_policy = policy


class BaseCase(unittest.TestCase):

    """
    Base test case. Handles common test setup.
    """

    def setUp(self):
        """Set up test data."""
        self.db_key = 'couchauth.db'
        self.db_default = 'auth'
        self.secret_key = 'couchauth.secret'
        self.secret_default = 'secret'
        self.user_names_view_default = 'pyramid/user_names'
        self.user_groups_view_default = 'pyramid/user_groups'
        self.user_perms_view_default = None
        self.group_perms_view_default = 'pyramid/group_perms'
        self.perm_users_view_default = None
        self.perm_groups_view_default = 'pyramid/perm_groups'
        self.settings_default = {}
        self.db_custom = 'auth_custom'
        self.secret_custom = 'Weez6ru2'
        self.user_names_view_custom = 'auth/user_names'
        self.user_groups_view_custom = 'auth/user_groups'
        self.user_perms_view_custom = 'auth/user_perms'
        self.group_perms_view_custom = 'auth/group_perms'
        self.perm_users_view_custom = 'auth/perm_users'
        self.perm_groups_view_custom = 'auth/perm_groups'
        self.settings_custom = {
            'couchauth.db': self.db_custom,
            'couchauth.secret': self.secret_custom,
            'couchauth.user_names_view': self.user_names_view_custom,
            'couchauth.user_groups_view': self.user_groups_view_custom,
            'couchauth.user_perms_view': self.user_perms_view_custom,
            'couchauth.group_perms_view': self.group_perms_view_custom,
            'couchauth.perm_users_view': self.perm_users_view_custom,
            'couchauth.perm_groups_view': self.perm_groups_view_custom}


class TestSession(BaseCase):
    
    """
    Test the session class.
    """

    def test_class(self):
        """Test the class attributes."""
        self.assertEqual(Session.db_key, self.db_key,
            'Session.db_key is invalid')
        self.assertEqual(Session.db_default, self.db_default,
            'Session.db_default is invalid')
        self.assertEqual(Session.secret_key, self.secret_key,
            'Session.secret_key is invalid')
        self.assertEqual(Session.secret_default, self.secret_default,
            'Session.secret_default is invalid')

    def test_init(self):
        """Test the __init__ method."""
        session = Session()
        self.assertFalse(session.configured,
            'session.configured is invalid')
        self.assertTrue(session.secret is None,
            'session.secret is invalid')
        self.assertTrue(session.dbname is None,
            'session.dbname is invalid')
        self.assertTrue(session._database is None,
            'session._database is invalid')

    def test_configure_defaults(self):
        """Test the configure method with default settings."""
        session = Session()
        session.configure(self.settings_default)
        self.assertEqual(session.dbname, self.db_default,
            'session.dbname is invalid')
        self.assertEqual(session.secret, self.secret_default,
            'session.secret is invalid')
        self.assertTrue(session._database is None,
            'session._database is invalid')
        self.assertTrue(session.configured,
            'session.configured is invalid')
        
    def test_configure_custom(self):
        """Test the configure method with custom settings."""
        session = Session()
        session.configure(self.settings_custom)
        self.assertEqual(session.dbname, self.db_custom,
            'session.dbname is invalid')
        self.assertEqual(session.secret, self.secret_custom,
            'session.secret is invalid')
        self.assertTrue(session._database is None,
            'session._database is invalid')
        self.assertTrue(session.configured,
            'session.configured is invalid')

    def test_database_get(self):
        """Test getting the database property."""
        session = Session()
        session.configure(self.settings_default)
        self.assertEqual(session.database.dbname, session.db_default,
            'getting session.database failed')

    def test_database_set(self):
        """Test setting the database property."""
        dbtest = "this is a test string"
        session = Session()
        session.configure(self.settings_default)
        session.database = dbtest
        self.assertEqual(session.database, dbtest,
            'setting session.database failed')


class TestModule(BaseCase):

    """
    Test the module functions and objects.
    """

    def test_session(self):
        """Test the pyramid_couchauth.session object."""
        self.assertIsInstance(pyramid_couchauth.session, Session,
            'pyramid_couchauth.session is invalid')

    def test_configure_default(self):
        """Test the configure function with default settings."""
        config = DummyConfig(self.settings_default)
        pyramid_couchdb.configure(config)
        pyramid_couchauth.configure(config)

        policy = config.authentication_policy
        self.assertIsInstance(policy, CouchAuthenticationPolicy,
            'authentication_policy object has invalid type')
        self.assertEqual(policy.database.dbname, self.db_default,
            'authentication_policy.database is invalid')
        self.assertEqual(policy.identifier.cookie.secret, self.secret_default,
            'authentication_policy.identifier.secret is invalid')
        self.assertEqual(policy.user_names_view,
            self.user_names_view_default,
            'authentication_policy.user_names_view is invalid')
        self.assertEqual(policy.user_groups_view,
            self.user_groups_view_default,
            'authentication_policy.user_groups_view is invalid')

        policy = config.authorization_policy
        self.assertIsInstance(policy, CouchAuthorizationPolicy,
            'authorization_policy object has invalid type')
        self.assertEqual(policy.database.dbname, self.db_default,
            'authorization_policy.database is invalid')
        self.assertEqual(policy.user_perms_view,
            self.user_perms_view_default,
            'authorization_policy.user_perms_view is invalid')
        self.assertEqual(policy.group_perms_view,
            self.group_perms_view_default,
            'authorization_policy.group_perms_view is invalid')
        self.assertEqual(policy.perm_users_view,
            self.perm_users_view_default,
            'authorization_policy.perm_users_view is invalid')
        self.assertEqual(policy.perm_groups_view,
            self.perm_groups_view_default,
            'authorization_policy.perm_groups_view is invalid')

    def test_configure_custom(self):
        """Test the configure function with custom settings."""
        config = DummyConfig(self.settings_custom)
        pyramid_couchdb.configure(config)
        pyramid_couchauth.configure(config)

        policy = config.authentication_policy
        self.assertIsInstance(policy, CouchAuthenticationPolicy,
            'authentication_policy object has invalid type')
        self.assertEqual(policy.database.dbname, self.db_custom,
            'authentication_policy.database is invalid')
        self.assertEqual(policy.identifier.cookie.secret, self.secret_custom,
            'authentication_policy.identifier.secret is invalid')
        self.assertEqual(policy.user_names_view,
            self.user_names_view_custom,
            'authentication_policy.user_names_view is invalid')
        self.assertEqual(policy.user_groups_view,
            self.user_groups_view_custom,
            'authentication_policy.user_groups_view is invalid')

        policy = config.authorization_policy
        self.assertIsInstance(policy, CouchAuthorizationPolicy,
            'authorization_policy object has invalid type')
        self.assertEqual(policy.database.dbname, self.db_custom,
            'authorization_policy.database is invalid')
        self.assertEqual(policy.user_perms_view,
            self.user_perms_view_custom,
            'authorization_policy.user_perms_view is invalid')
        self.assertEqual(policy.group_perms_view,
            self.group_perms_view_custom,
            'authorization_policy.group_perms_view is invalid')
        self.assertEqual(policy.perm_users_view,
            self.perm_users_view_custom,
            'authorization_policy.perm_users_view is invalid')
        self.assertEqual(policy.perm_groups_view,
            self.perm_groups_view_custom,
            'authorization_policy.perm_groups_view is invalid')

