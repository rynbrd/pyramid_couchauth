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
from pyramid.interfaces import IAuthorizationPolicy
from pyramid.security import Everyone
from pyramid_couchauth.principal import Principal

class CouchAuthorizationPolicy:
    """CouchDB authorization policy."""
    implements(IAuthorizationPolicy)

    def __init__(self, database,
            user_perms_view=None,
            group_perms_view='pyramid/group_perms',
            perm_users_view=None,
            perm_groups_view='pyramid/perm_groups'):
        """
        Initialize the authorization policy.
        :param translations: The CouchDB to object translations.
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
        :param context: The context to check the principal's permission
            against. 
        :param principals: The list of principals to check.
        :param permission: The permission to check.
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
        :param context: The context to check permissions in.
        :param permission: The permission to retrieve principals for.
        :return: A list of principals.
        """
        principals = []
        if self.perm_users_view is not None:
            users = self.database.view(self.perm_users_view, key=permission)
            pstrs = [str(Principal(type='user', name=user)) for user in users]
            principals.extend(pstrs)
        if self.perm_groups_view is not None:
            groups = self.database.view(self.perm_groups_view, key=permission)
            pstrs = [str(Principal(type='group', name=group)) for group in groups]
            principals.extend(pstrs)
        return principals

