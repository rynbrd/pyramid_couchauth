# Copyright (c) 2011-2012, Ryan Bourgeois <bluedragonx@gmail.com>
# All rights reserved.
#
# This software is licensed under a modified BSD license as defined in the
# provided license file at the root of this project.  You may modify and/or
# distribute in accordance with those terms.
#
# This software is provided "as is" and any express or implied warranties,
# including, but not limited to, the implied warranties of merchantability and
# fitness for a particular purpose are disclaimed.
"""
Identification implementations.
"""

from zope.interface import implementer
from pyramid.authentication import AuthTktCookieHelper
from pyramid_couchauth.interfaces import IIdentifier


@implementer(IIdentifier)
class AuthTktIdentifier:

    """
    An identifier for storing the currently authenticated principal in an
    authtkt cookie. Uses pyramid.authentication.AuthTktCookieHelper.
    """

    def __init__(self, secret, cookie_name='auth_tkt', secure=False,
        include_ip=False, timeout=None, reissue_time=None, max_age=None,
        path="/", http_only=False, wild_domain=True):
        """
        Initialize the identifier. Takes the same arguments as
        pyramid.authentication.AuthTktCookieHelper.
        """
        self.cookie = AuthTktCookieHelper(secret, cookie_name=cookie_name,
            secure=secure, include_ip=include_ip, timeout=timeout,
            reissue_time=reissue_time, max_age=max_age, http_only=http_only,
            path=path, wild_domain=wild_domain)

    def identify(self, request):
        """
        Return the username of the remembered user.

        :param request: The WSGI request.
        :return: The username of the remembered user.
        """
        identifier = self.cookie.identify(request)
        return identifier['userid'] if identifier else None

    def remember(self, request, username, **kw):
        """
        Return the headers necessary for remembering the principal.

        :param request: The WSGI request.
        :param username: The username to remember.
        :param kw: Additional identifier parameters.
        :return: A list of headers to add to the response.
        """
        return self.cookie.remember(request, username, **kw)

    def forget(self, request):
        """
        Return the headers necessary for forgetting any remembered principal.

        :param request: The WSGI request.
        :return: A list of headers to add to the response.
        """
        return self.cookie.forget(request)

