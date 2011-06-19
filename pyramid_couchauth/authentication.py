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

from zope.interface import implements
from pyramid.interfaces import IAuthenticationPolicy
from pyramid.security import Authenticated, Everyone
from pyramid_couchauth.principal import Principal

class CouchAuthenticationPolicy:
    """CouchDB authentication policy."""
    implements(IAuthenticationPolicy)

    def __init__(self, database, identifier,
            user_names_view='pyramid/user_names',
            user_groups_view='pyramid/user_groups'):
        """
        Initialize the authentication policy.
        :param translations: The CouchDB to object translations.
        :param identifier: The identifier object to use.
        """
        self.identifier = identifier
        self.database = database
        self.user_names_view = user_names_view
        self.user_groups_view = user_groups_view

    def _expand_principal(self, principal):
        """
        Expand a user principal into a list of user and group principals.
        :param principal: The user principal to expand.
        :return: A list of principals or an empty list of the given principal
            did not exist.
        """
        principals = []
        pobj = Principal(principal)
        users = self.database.view(self.user_names_view, key=pobj.name)

        if len(users) > 0:
            principals.append(Authenticated)
            principals.append(str(pobj))

            groups = self.database.view(self.user_groups_view, key=pobj.name)
            for group in groups:
                principals.append(str(Principal(type='group', name=group['value'])))
        return principals

    def unauthenticated_userid(self, request):
        """
        Retrieve a user ID for use when none is authenticated.
        :param request: The WSGI request.
        :return: The 
        """
        return self.identifier.identity(request)

    def authenticated_userid(self, request):
        """
        Retrieve the authenticated user ID.
        :param request: The WSGI request.
        :return: A string containing the principal of the authenticated user or
            None if no user is authenticated.
        """
        username = self.unauthenticated_userid(request)
        if username is not None:
            users = self.database.view(self.user_names_view, key=username)
            if len(users) > 0:
                return username
        return None

    def effective_principals(self, request):
        """
        Retrieve the effected principals.
        :param request: The WSGI request.
        :return: A list of effected users and groups.
        """
        principals = [Everyone]
        identity = self.unauthenticated_userid(request)
        if identity is not None:
            principals.extend(self._expand_principal(identity))
        return principals

    def remember(self, request, principal, **kw):
        """
        Return a set of headers suitable for "remembering" the given principal.
        :param request: The WSGI request.
        :param principal: The principal to remember.
        :param kw: Additional parameters.
        :return: A list of headers.
        """
        return self.identifier.remember(request, principal, **kw)

    def forget(self, request):
        """
        Return a set of headers suitable for "forgetting" the current user
        principal.
        :param request: The WSGI request.
        :return: A list of headers.
        """
        return self.identifier.forget(request)

