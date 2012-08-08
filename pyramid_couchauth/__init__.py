# Copyright (c) 2011-2012 Ryan Bourgeois <bluedragonx@gmail.com>
#
# This project is free software according to the BSD-modified license. Refer to
# the LICENSE file for complete details.
"""
Implements auth/auth support in Pyramid against CouchDB.
"""


class Session:

    """
    Store session information.
    """

    db_key = 'couchauth.db'
    db_default = 'auth'
    secret_key = 'couchauth.secret'
    secret_default = 'secret'

    def __init__(self):
        """
        Initialize the object.
        """
        self.configured = False
        self.secret = None
        self.dbname = None
        self._database = None

    def configure(self, settings):
        """
        Configure the session. Attempts to retrieve the database name from
        couchauth.db and the shared secret from couchauth.secret.
        """
        self.dbname = self.db_default
        if self.db_key in settings:
            self.dbname = settings[self.db_key]
        self._database = None

        if self.secret_key in settings:
            self.secret = settings[self.secret_key]
        else:
            self.secret = self.secret_default

        self.configured = True

    @property
    def database(self):
        """The auth/auth database."""
        if self._database is None:
            import pyramid_couchdb
            self._database = pyramid_couchdb.session.server.get_db(self.dbname)
        return self._database

    @database.setter
    def database(self, database):
        """The auth/auth database."""
        self._database = database


session = Session()


def configure(config):
    """
    Configure Pyramid to use couchauth.

    :param config: The pyramid config object.

    Settings:
        couchauth.secret -- The shared secret. If not None it overrides the
            value in the session object.
        couchauth.db -- The auth/auth database. If not None it overrides the
            value in the session object.
        couchauth.user_names_view -- A view which maps the username as the key.
            The value may be anything as this view is only used to validate the
            existance of a user. Defaults to 'pyramid/user_names'.
        couchauth.user_groups_view -- A view which maps group names (the value)
            to their member usernames (the key). This view is used to expand a
            user principal into group principals. Defaults to
            'pyramid/user_groups'.
        couchauth.user_perms_view -- A view which maps permission names (the
            values) to usernames (the keys). A None value disables direct user
            permission mapping. This is useful when using groups for all
            permission controls. Defaults to None.
        couchauth.group_perms_view -- A view which maps permission names (the
            values) to group names (the keys). A None value disables group
            permission mapping. This is useful if you wish all permissions to
            be controlled at the user level. Defaults to 'pyramid/group_perms'.
        couchauth.perm_users_view -- A view which maps usernames (the values)
            to permission names (the keys). A None value disables permission
            user mapping. This is useful when using groups for all permission
            controls. Defaults to None.
        couchauth.perm_groups_view -- A view which maps group names (the
            values) to permission names (the keys). A None value disables
            permission group mapping. This is useful if you wish all
            permissions to be controlled at the user level. Defaults to
            'pyramid/perm_groups'.
    """
    settings = config.get_settings()
    session.configure(settings)

    def setting(key, default=None):
        if key in settings and settings[key]:
            return settings[key]
        return default

    from pyramid_couchauth.identification import AuthTktIdentifier
    from pyramid_couchauth.policies import (CouchAuthenticationPolicy,
        CouchAuthorizationPolicy)

    identifier = AuthTktIdentifier(session.secret)
    authentication = CouchAuthenticationPolicy(session.database, identifier,
        setting('couchauth.user_names_view', 'pyramid/user_names'),
        setting('couchauth.user_groups_view', 'pyramid/user_groups'))
    authorization = CouchAuthorizationPolicy(session.database,
        setting('couchauth.user_perms_view'),
        setting('couchauth.group_perms_view', 'pyramid/group_perms'),
        setting('couchauth.perm_users_view'),
        setting('couchauth.perm_groups_view', 'pyramid/perm_groups'))

    config.set_authentication_policy(authentication)
    config.set_authorization_policy(authorization)
    return config

