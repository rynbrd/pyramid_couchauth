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
        Creates a new CouchDB authentication policy object.
        :param database: The database where authentication data is stored.
        :param user_names_view: A view which maps the username as the key. The
            value may be anything as this view is only used to validate the
            existance of a user.
        :param user_groups_view: A view which maps group names (the value) to
            their member usernames (the key). This view is used to expand a
            user principle into group principals.
        :param identifier: The identifier object to use. The identifier is used
            to store authenticated user information. It must implement the
            IIdentifier interface.
        """
        self.identifier = identifier
        self.database = database
        self.user_names_view = user_names_view
        self.user_groups_view = user_groups_view

    def _expand_principal(self, principal):
        """
        Expand a user principal into a list of principals. If the user exists
        then the resulting list will contain the Authenticated principal, the
        user principal, and a principal for each group the user belongs to.
        :param principal: The user principal to expand.
        :return: The list of expanded principals. The list will be empty if the
            user does not exist.
        """
        principals = []
        pobj = Principal(principal, 'user')
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
        Retrieve an unauthenticated username. Calls the underlying identifier.
        :param request: The WSGI request.
        :return: The unauthenticated username or None if no user is present.
        """
        return self.identifier.identity(request)

    def authenticated_userid(self, request):
        """
        Retrieve the authenticated user ID. Calls the underlying identifier and
        validates the results.
        :param request: The WSGI request.
        :return: The username of the authenticated user or None if no user is
            authenticated.
        """
        username = self.unauthenticated_userid(request)
        if username is not None:
            users = self.database.view(self.user_names_view, key=username)
            if len(users) > 0:
                return username
        return None

    def effective_principals(self, request):
        """
        Retrieve the effective principals for the current request.
        :param request: The WSGI request.
        :return: A list of principles.
        """
        principals = [Everyone]
        username = self.unauthenticated_userid(request)
        if username is not None:
            principals.extend(self._expand_principal(username))
        return principals

    def remember(self, request, principal, **kw):
        """
        Return a set of headers suitable for "remembering" the given principal.
        This calls the underlying identifier.
        :param request: The WSGI request.
        :param principal: The principal to remember.
        :param kw: Additional parameters.
        :return: A list of headers.
        """
        pobj = Principle(principal, 'user')
        return self.identifier.remember(request, pobj.name, **kw)

    def forget(self, request):
        """
        Return a set of headers suitable for "forgetting" the current user
        principal. This calls the underlying identifier.
        :param request: The WSGI request.
        :return: A list of headers.
        """
        return self.identifier.forget(request)

