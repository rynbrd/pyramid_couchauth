# Copyright (c) 2011-2012 Ryan Bourgeois <bluedragonx@gmail.com>
#
# This project is free software according to the BSD-modified license. Refer to
# the LICENSE file for complete details.
"""
Test identifiers.
"""

import re
import unittest
from pyramid import testing
from pyramid import authentication as auth
from pyramid_couchauth.interfaces import IIdentifier
from pyramid_couchauth.identification import AuthTktIdentifier


class TestAuthTktIdentifier(unittest.TestCase):

    """Test the AuthTktIdentifier class."""

    def test_interface(self):
        """Verify AuthTktIdentifier implements the identifier interface."""
        self.assertTrue(IIdentifier.implementedBy(AuthTktIdentifier))

    def test_init(self):
        """Verify __init__ operates as expected."""
        secret = 'test_auth_tkt_secret'
        identifier = AuthTktIdentifier(secret=secret)
        self.assertEqual(identifier.cookie.secret, secret,
            'secret parameter set incorrectly')
        self.assertEqual(identifier.cookie.cookie_name, 'auth_tkt',
            'cookie_name default value incorrect')
        self.assertEqual(identifier.cookie.secure, False,
            'secure default value incorrect')
        self.assertEqual(identifier.cookie.include_ip, False,
            'include_ip default value incorrect')
        self.assertEqual(identifier.cookie.timeout, None,
            'timeout default value incorrect')
        self.assertEqual(identifier.cookie.reissue_time, None,
            'reissue_time default value incorrect')
        self.assertEqual(identifier.cookie.max_age, None,
            'max_age default value incorrect')
        self.assertEqual(identifier.cookie.path, '/',
            'path default value incorrect')
        self.assertEqual(identifier.cookie.http_only, False,
            'http_only default value incorrect')
        self.assertEqual(identifier.cookie.wild_domain, True,
            'wild_domain default value incorrect')

    def test_identify_absent(self):
        """Verify return of identify when no cookie is present."""
        request = testing.DummyRequest()
        identifier = AuthTktIdentifier('secret')
        self.assertEqual(identifier.identify(request), None,
            'identification found for null cookie')

    def test_identity_present(self):
        """Verify return of identify when cookie is present."""
        secret = 'secret'
        domain = 'localhost'
        remote_addr = '0.0.0.0'
        username = 'user'

        request = testing.DummyRequest()
        request.environ['HTTP_HOST'] = domain
        request.environ['REMOTE_ADDR'] = remote_addr
        identifier = AuthTktIdentifier('secret')
        headers = identifier.remember(request, username)
        name = headers[0][0]
        cookie = re.sub(';.*', '', headers[0][1][len(name)-1:]).strip('"')
        request.cookies = {'auth_tkt': cookie}

        self.assertEqual(identifier.identify(request), username,
            'unable to identify user')

    def test_remember(self):
        """Verify the headers generated when calling remember."""
        domain = 'localhost'
        header_name = 'Set-Cookie'
        header_value = re.compile(
            '^auth_tkt="[a-zA-Z0-9%]+!userid_type:b64str"; ' +
            'Path=/(; Domain=\.?' + domain + ')?$')
        request = testing.DummyRequest()
        request.environ['HTTP_HOST'] = domain
        identifier = AuthTktIdentifier('secret')
        headers = identifier.remember(request, 'user')

        for header in headers:
            self.assertEqual(header[0], header_name,
                'remember header name invalid')
            self.assertTrue(header_value.match(header[1]),
                'remember header value invalid')

    def test_forget(self):
        """Verify the headers generated when calling forget."""
        domain = 'localhost'
        header_name = 'Set-Cookie'
        header_value = re.compile(
            '^auth_tkt=""; Path=/; (Domain=\.?' + domain +
            '; )?Max-Age=0; Expires=.*$')
        request = testing.DummyRequest()
        request.environ['HTTP_HOST'] = domain
        identifier = AuthTktIdentifier('secret')
        headers = identifier.forget(request)

        for header in headers:
            self.assertEqual(header[0], header_name,
                'forget header name invalid')
            self.assertTrue(header_value.match(header[1]),
                'forget header value invalid')

