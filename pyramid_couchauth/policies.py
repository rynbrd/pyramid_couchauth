# Copyright (c) 2011-2012 Ryan Bourgeois <bluedragonx@gmail.com>
#
# This project is free software according to the BSD-modified license. Refer to
# the LICENSE file for complete details.
"""
Policies for auth/auth against CouchDB.
"""

from zope.interface import implementer
from pyramid.interfaces import IAuthenticationPolicy, IAuthorizationPolicy
from pyramid.security import Authenticated, Everyone
from pyramid_couchauth.principals import Principal


__all__ = ['CouchAuthenticationPolicy', 'CouchAuthorizationPolicy']


@implementer(IAuthenticationPolicy)
class CouchAuthenticationPolicy(object):

    """CouchDB authentication policy."""

    def __init__(self, database, identifier,
            user_names_view='pyramid/user_names',
            user_groups_view='pyramid/user_groups'):
        """
        Create a new CouchDB authentication policy object.

        :param database: The database where authentication data is stored.
        :param identifier: The identifier object to use. The identifier is used
            to store authenticated user information. It must implement the
            IIdentifier interface.
        :param user_names_view: A view which maps the username as the key. The
            value may be anything as this view is only used to validate the
            existance of a user. Defaults to 'pyramid/user_names'.
        :param user_groups_view: A view which maps group names (the value) to
            their member usernames (the key). This view is used to expand a
            user principal into group principals. Defaults to
            'pyramid/user_groups'.
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
        return self.identifier.identify(request)

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
        :return: A list of principals.
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
        pobj = Principal(principal, 'user')
        return self.identifier.remember(request, pobj.name, **kw)

    def forget(self, request):
        """
        Return a set of headers suitable for "forgetting" the current user
        principal. This calls the underlying identifier.
        :param request: The WSGI request.
        :return: A list of headers.
        """
        return self.identifier.forget(request)


@implementer(IAuthorizationPolicy)
class CouchAuthorizationPolicy(object):

    """CouchDB authorization policy."""

    def __init__(self, database,
            user_perms_view=None,
            group_perms_view='pyramid/group_perms',
            perm_users_view=None,
            perm_groups_view='pyramid/perm_groups'):
        """
        Creates a new CouchDB authorization policy.
        :param database: The database where authorization data is stored.
        :param user_perms_view: A view which maps permission names (the values)
            to usernames (the keys). A None value disables direct user
            permission mapping. This is useful when using groups for all
            permission controls. Defaults to None.
        :param group_perms_view: A view which maps permission names (the
            values) to group names (the keys). A None value disables group
            permission mapping. This is useful if you wish all permissions to
            be controlled at the user level. Defaults to 'pyramid/group_perms'.
        :param perm_users_view: A view which maps usernames (the values) to
            permission names (the keys). A None value disables permission user
            mapping. This is useful when using groups for all permission
            controls.  Defaults to None.
        :param perm_groups_view: A view which maps group names (the values) to
            permission names (the keys). A None value disables permission group
            mapping. This is useful if you wish all permissions to be
            controlled at the user level. Defaults to 'pyramid/perm_groups'.
        """
        self.database = database
        self.user_perms_view = user_perms_view
        self.group_perms_view = group_perms_view
        self.perm_users_view = perm_users_view
        self.perm_groups_view = perm_groups_view

    def permits(self, context, principals, permission):
        """
        Return True if any of the principals have the provided permission in
        the given context. Return False otherwise.
        :param context: The context in which permission checking is occuring.
        :param principals: The list of principals to check.
        :param permission: The permission to check the principals for.
        :return: True if one of the principals has the permission, false
            otherwise.
        """
        for principal in principals:
            if principal == Everyone:
                pobj = Principal(type='user', name=Everyone)
            else:
                pobj = Principal(principal)
            if pobj.type == 'user' and self.user_perms_view is not None:
                perms = self.database.view(self.user_perms_view, key=pobj.name)
                for perm in perms:
                    if perm['value'] == permission:
                        return True
            elif pobj.type == 'group' and self.group_perms_view is not None:
                perms = self.database.view(self.group_perms_view, key=pobj.name)
                for perm in perms:
                    if perm['value'] == permission:
                        return True
        return False

    def principals_allowed_by_permission(self, context, permission):
        """
        Return a list of principals who have the provided permission in the
        given context.
        :param context: The context in which permission checking is occuring.
        :param permission: The permission to retrieve principals for.
        :return: A list of principals which contain the given permission.
        """
        principals = []
        if self.perm_users_view is not None:
            users = self.database.view(self.perm_users_view, key=permission)
            pstrs = [str(Principal(type='user', name=user['value'])) for user in users]
            principals.extend(pstrs)
        if self.perm_groups_view is not None:
            groups = self.database.view(self.perm_groups_view, key=permission)
            pstrs = [str(Principal(type='group', name=group['value'])) for group in groups]
            principals.extend(pstrs)
        return principals

