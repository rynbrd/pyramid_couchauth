# Copyright (c) 2011-2012 Ryan Bourgeois <bluedragonx@gmail.com>
#
# This project is free software according to the BSD-modified license. Refer to
# the LICENSE file for complete details.
"""
Implement authentication principals.
"""


class Principal:

    """
    Abstracts an auth principal. Principals can be users, groups, or even other
    entities. This class allows the principal to carry its type with it.
    """

    def __init__(self, principal=None, type=None, name=None):
        """
        Create a new Principal object.

        :param principal: A full principal string. Overrides type and name if
            given as part of the string.
        :param type: The type of the principal.
        :param name: The name of the principal.
        """
        self.type = type
        self.name = name
        if principal is not None:
            self.parse(principal)

    def parse(self, principal):
        """
        Parses a principal string and saves it in the object.

        :param principal: A string containing the locally formatted principal.
        """
        p = principal.partition(':')
        if p[1] == '':
            self.name = p[0]
        else:
            self.type = p[0]
            self.name = p[2]

    def __str__(self):
        """
        Convert the Principal object to a string.
        """
        return '%s:%s' % (self.type, self.name)

    def __repr__(self):
        """
        Create a string representation of the object.
        """
        esc = lambda s: s.replace("'", "\\'")
        params = []
        if self.type is not None:
            params.append("type='%s'" % esc(self.type))
        if self.name is not None:
            params.append("name='%s'" % esc(self.name))
        return '<Principal(%s)>' % ', '.join(params)

