# Copyright (c) 2011-2012 Ryan Bourgeois <bluedragonx@gmail.com>
#
# This project is free software according to the BSD-modified license. Refer to
# the LICENSE file for complete details.
"""
Test Couch auth/auth policies.
"""

import re
import unittest
from pyramid.testing import DummyRequest
from pyramid.security import Authenticated, Everyone
from pyramid_couchauth.principal import Principal
from pyramid_couchauth.identification import AuthTktIdentifier
from pyramid_couchauth.policies import (CouchAuthenticationPolicy,
    CouchAuthorizationPolicy)
from tests.couch import DummyDatabase


class TestPolicy(unittest.TestCase):

    """Base test case. Sets up dummy database with test data."""

    def setUp(self):
        """Set up the policy test."""
        self.database = DummyDatabase({})
        self.database.add_view('pyramid/user_names', {
            'admin': ['admin']})
        self.database.add_view('pyramid/user_groups', {
            'admin': ['administrators']})
        self.database.add_view('pyramid/group_perms', {
            'administrators': ['superpowers']})
        self.database.add_view('pyramid/perm_groups', {
            'superpowers': ['administrators']})

    def tearDown(self):
        """Tear down the policy test."""


class TestCouchAuthenticationPolicy(TestPolicy):

    """
    Test the CouchAuthenticationPolicy class.
    """

    def setUp(self):
        """Build dummy objects for use with the test case."""
        TestPolicy.setUp(self)

        self.secret = 'secret'
        self.domain = 'localhost'
        self.remote_addr = '0.0.0.0'
        self.username = 'admin'

        self.identifier = AuthTktIdentifier(self.secret)
        self.policy = CouchAuthenticationPolicy(self.database, self.identifier)

        self.request = DummyRequest()
        self.request.environ['HTTP_HOST'] = self.domain
        self.request.environ['REMOTE_ADDR'] = self.remote_addr
        headers = self.identifier.remember(self.request, self.username)
        cookie = re.sub(';.*', '', headers[0][1][len(headers[0][0])-1:]).strip('"')
        self.request.cookies = {'auth_tkt': cookie}

    def test_init(self):
        """Test the __init__ method."""
        self.assertEqual(self.policy.identifier, self.identifier,
            'identifier not set to parameter value')
        self.assertEqual(self.policy.database, self.database,
            'database not set to parameter value')
        self.assertEqual(self.policy.user_names_view, 'pyramid/user_names',
            'user_names_view not set to default value')
        self.assertEqual(self.policy.user_groups_view, 'pyramid/user_groups',
            'user_groups_view not set to default value')

    def test_expand_principal(self):
        """Test the _expand_principal method."""
        expected = set([Authenticated, 'user:admin', 'group:administrators'])
        principals = set(self.policy._expand_principal('admin'))
        self.assertEqual(principals, expected,
            'expanded principals invalid')

    def test_unauthenticated_userid(self):
        """Test the unauthenticated_userid method."""
        self.assertEqual(self.policy.unauthenticated_userid(self.request),
            self.username, 'invalid unauthenticated userid')

    def test_authenticated_userid(self):
        """Test the authenticated_userid method."""
        self.assertEqual(self.policy.authenticated_userid(self.request),
            self.username, 'invalid authenticated userid')

    def test_effective_principals(self):
        """Test the effective_principals method."""
        expected = set([Authenticated, Everyone, 'user:admin', 'group:administrators'])
        principals = set(self.policy.effective_principals(self.request))
        self.assertEqual(principals, expected,
            'effective principals invalid')

    def test_remember(self):
        """Test the remember method."""
        header_name = 'Set-Cookie'
        header_value = re.compile(
            '^auth_tkt="[a-zA-Z0-9%]+!userid_type:b64str"; ' +
            'Path=/(; Domain=\.?' + self.domain + ')?$')

        headers = self.policy.remember(self.request, self.username)
        for header in headers:
            self.assertEqual(header[0], header_name,
                'remember header name invalid')
            self.assertTrue(header_value.match(header[1]),
                'remember header value invalid')

    def test_forget(self):
        """Test the forget method."""
        header_name = 'Set-Cookie'
        header_value = re.compile(
            '^auth_tkt=""; Path=/; (Domain=\.?' + self.domain +
            '; )?Max-Age=0; Expires=.*$')

        headers = self.policy.forget(self.request)
        for header in headers:
            self.assertEqual(header[0], header_name,
                'forget header name invalid')
            self.assertTrue(header_value.match(header[1]),
                'forget header value invalid')


class TestCouchAuthorizationPolicy(TestPolicy):

    """
    Test the CouchAuthorizationPolicy class.
    """

    def setUp(self):
        """Build dummy objects for use with the test case."""
        TestPolicy.setUp(self)
        self.context = {}
        self.policy = CouchAuthorizationPolicy(self.database)

    def test_init(self):
        """Test the __init__ method."""
        self.assertEqual(self.policy.database, self.database,
            'database not set to parameter value')
        self.assertTrue(self.policy.user_perms_view is None,
            'user_perms_view not set to default value')
        self.assertEqual(self.policy.group_perms_view, 'pyramid/group_perms',
            'group_perms_view not set to default value')
        self.assertTrue(self.policy.perm_users_view is None,
            'perm_users_view not set to default value')
        self.assertEqual(self.policy.perm_groups_view, 'pyramid/perm_groups',
            'perm_groups_view not set to default value')

    def test_permits_allow(self):
        """Test the permits method when permission is granted."""
        principal = Principal(type='user', name='admin')r
        self.assertTrue(self.policy.permits(self.context, [str(principal)],
            'superpowers'), 'admin does not have superpowers')

    def test_permits_deny(self):
        """Test the permits method when permission is denied."""
        principal = Principal(type='user', name='admin')
        self.assertFalse(self.policy.permits(self.context, [str(principal)],
            'godmode'), 'admin has godmode')

    def test_principals_allowed_by_permission_present(self):
        """Test the principals_allowed_by_permission when results exist."""
        principal = Principal(type='group', name='administrators')
        expect = set([str(principal)])
        found = set(self.policy.principals_allowed_by_permission(self.context,
            'superpowers'))
        self.assertEqual(expect, found,
            'invalid principals for superpowers permission')

    def test_principals_allowed_by_permission_absent(self):
        """Test the principals_allowed_by_permission when results do not exist."""
        expect = set([])
        found = set(self.policy.principals_allowed_by_permission(self.context,
            'godmode'))
        self.assertEqual(expect, found,
            'invalid principals for godmode permission')

