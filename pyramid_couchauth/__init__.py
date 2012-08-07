# Copyright (c) 2011-2012 Ryan Bourgeois <bluedragonx@gmail.com>
#
# This project is free software according to the BSD-modified license. Refer to
# the LICENSE file for complete details.
"""
Implements auth/auth support in Pyramid against CouchDB.
"""


def configure(config, database user_names_view='pyramid/user_names',
        user_groups_view='pyramid/user_groups', user_perms_view=None,
        group_perms_view='pyramid/group_perms', perm_users_view=None,
        perm_groups_view='pyramid/perm_groups'):
    """
    Load Pyramid with the couchauth auth/auth policies.

    Settings:
      couchauth.secret -- The shared secret used by the AuthTkt identifier.

    :param config: The Pyramid config object.
    :param database: The couchdbkit database containing the authentication
        views.
    :param user_names_view: A view which maps the username as the key. The
        value may be anything as this view is only used to validate the
        existance of a user. Defaults to 'pyramid/user_names'.
    :param user_groups_view: A view which maps group names (the value) to
        their member usernames (the key). This view is used to expand a
        user principal into group principals. Defaults to
        'pyramid/user_groups'.
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
    settings = config.get_settings()

    def get_setting(name, default=None):
        if name in settings:
            return settings[name]
        else:
            return default

    from pyramid_couchauth.identification import AuthTktIdentifier
    from pyramid_couchauth.policies import (CouchAuthenticationPolicy,
        CouchAuthorizationPolicy)

    secret = get_setting('couchauth.secret', 'secret')
    identifier = AuthTktIdentifier(secret)
    authentication = CouchAuthenticationPolicy(database, identifier)
    authorization = CouchAuthorizationPolicy(database)

    config.set_authentication_policy(authentication)
    config.set_authorization_policy(authorization)
    return config

