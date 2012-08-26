# Copyright (c) 2011-2012 Ryan Bourgeois <bluedragonx@gmail.com>
#
# This project is free software according to the BSD-modified license. Refer to
# the LICENSE file for complete details.
"""
Dummy CouchDB database objects.
"""

class DummyDatabase(object):

    """
    Pretend to be a CouchDB database.
    """

    def __init__(self, data):
        """Initialize the object."""
        self.data = data
        self.views = {}

    def add_view(self, name, data):
        """Add view data to the dummy database."""
        self.views[name] = data

    def view(self, name, key):
        """Get a value out of a view."""
        if name not in self.views or key not in self.views[name]:
            return []
        return [{'value': v} for v in self.views[name][key]]

