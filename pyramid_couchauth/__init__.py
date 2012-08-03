# Copyright (c) 2011-2012 Ryan Bourgeois <bluedragonx@gmail.com>
#
# This project is free software according to the BSD-modified license. Refer to
# the LICENSE file for complete details.
"""
Implements auth/auth support in Pyramid against CouchDB.
"""

def configure(config, database):
    """
    Load Pyramid with the couchauth auth/auth policies.

    Settings:
      couchauth.secret -- The shared secret used by the AuthTkt identifier.

    :param config: The Pyramid config object.
    :param database: The couchdbkit database containing the authentication
        views.
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

