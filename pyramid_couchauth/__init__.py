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


def configure(config, secret=None, database=None):
    """
    Configure Pyramid to use couchauth.

    :param config: The pyramid config object.
    :param secret: The shared secret. If not None it overrides the value in the
        session object.
    :param database: The auth/auth database. If not None it overrides the value
        in the session object.
    """
    settings = config.get_settings()
    session.configure(settings)
    if secret is not None:
        session.secret = secret
    if database is not None:
        if isinstance(database, basestring):
            import pyramid_couchdb
            database = pyramid_couchdb.session.server.get_db(database)
        session.database = database

    from pyramid_couchauth.identification import AuthTktIdentifier
    from pyramid_couchauth.policies import (CouchAuthenticationPolicy,
        CouchAuthorizationPolicy)

    identifier = AuthTktIdentifier(session.secret)
    authentication = CouchAuthenticationPolicy(session.database, identifier)
    authorization = CouchAuthorizationPolicy(session.database)

    config.set_authentication_policy(authentication)
    config.set_authorization_policy(authorization)
    return config

