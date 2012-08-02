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

