# Copyright (c) 2011-2012 Ryan Bourgeois <bluedragonx@gmail.com>
#
# This project is free software according to the BSD-modified license. Refer to
# the LICENSE file for complete details.
"""
Test the principal module.
"""

import unittest
from pyramid_couchauth.principal import Principal


class TestPrincipal(unittest.TestCase):

    """
    Test the Principal class.
    """

    def setUp(self):
        """Initialize test values."""
        self.type = 'user'
        self.name = 'test'
        self.principal = 'user:test'
        self.repr_type = "<Principal(type='user')>"
        self.repr_name = "<Principal(name='test')>"
        self.repr_all = "<Principal(type='user', name='test')>"

    def test_init_empty(self):
        """Test __init__ method with no params."""
        pobj = Principal()
        self.assertTrue(pobj.type is None)
        self.assertTrue(pobj.name is None)

    def test_init_type_name(self):
        """Test __init__ method with type and name params."""
        pobj = Principal(type=self.type, name=self.name)
        self.assertEqual(pobj.type, self.type)
        self.assertEqual(pobj.name, self.name)

    def test_init_principal(self):
        """Test __init__ method with principal param."""
        pobj = Principal(self.principal)
        self.assertEqual(pobj.type, self.type)
        self.assertEqual(pobj.name, self.name)

    def test_init_type_principal(self):
        """Test __init__ method with type and principal params."""
        pobj = Principal(self.name, self.type)
        self.assertEqual(pobj.type, self.type)
        self.assertEqual(pobj.name, self.name)

    def test_parse(self):
        """Test parse method."""
        pobj = Principal()
        pobj.parse(self.principal)
        self.assertEqual(pobj.type, self.type)
        self.assertEqual(pobj.name, self.name)

    def test_str(self):
        """Test __str__ method."""
        pobj = Principal(self.principal)
        self.assertEqual(pobj.__str__(), self.principal)

    def test_repr_type(self):
        """Test __repr__ method when type is set."""
        pobj = Principal(type=self.type)
        self.assertEqual(pobj.__repr__(), self.repr_type)

    def test_repr_name(self):
        """Test __repr__ method when name is set."""
        pobj = Principal(name=self.name)
        self.assertEqual(pobj.__repr__(), self.repr_name)

    def test_repr_all(self):
        """Test __repr__ method when principal is set."""
        pobj = Principal(self.principal)
        self.assertEqual(pobj.__repr__(), self.repr_all)

