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

class Principal:
    """
    Abstracts an auth principal. Principals can be users, groups, or even other
    entities. This class allows the principal to carry its type with it.
    """

    def __init__(self, principal=None, type=None, name=None):
        """
        Create a new Principal object.
        :param principal: A full principal string. Overrides type and name if
            given.
        :param type: The type of the principal.
        :param name: The name of the principal.
        """
        if principal is not None:
            self.parse(principal)
        else:
            self.type = type
            self.name = name

    def parse(self, principal):
        """
        Parses a principal string and saves it in the object.
        :param principal: A string containing the locally formatted principle.
        """
        p = principal.partition(':')
        if p[1] == '':
            self.type = None
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
        Create a string representation of the object. Useful for debug output.
        """
        esc = lambda s: s.replace("'", "\\'")
        params = []
        if self.type is not None:
            params.append("type='%s'" % esc(self.type))
        if self.name is not None:
            params.append("name='%s'" % esc(self.name))
        return '<Principal(%s)>' % ', '.join(params)

