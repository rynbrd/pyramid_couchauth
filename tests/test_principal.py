# Copyright (c) 2010, Ryan Bourgeois <bluedragonx@gmail.com>
# All rights reserved.
#
# This software is licensed under a modified BSD license as defined in the
# provided license file at the root of this project.  You may modify and/or
# distribute in accordance with those terms.
#
# This software is provided "as is" and any express or implied warranties,
# including, but not limited to, the implied warranties of merchantability and
# fitness for a particular purpose are disclaimed.

import unittest
from pyramid_couchauth.principal import Principal

def suite():
    return unittest.defaultTestLoader.loadTestsFromTestCase(TestPrincipal)

class TestPrincipal(unittest.TestCase):

    def setUp(self):
        self.type = 'user'
        self.name = 'test'
        self.principal = 'user:test'
        self.repr_type = "<Principal(type='user')>"
        self.repr_name = "<Principal(name='test')>"
        self.repr_all = "<Principal(type='user', name='test')>"

    def tearDown(self):
        pass

    def test_init_empty(self):
        pobj = Principal()
        self.assertTrue(pobj.type is None)
        self.assertTrue(pobj.name is None)

    def test_init_type_name(self):
        pobj = Principal(type=self.type, name=self.name)
        self.assertEqual(pobj.type, self.type)
        self.assertEqual(pobj.name, self.name)

    def test_init_principal(self):
        pobj = Principal(self.principal)
        self.assertEqual(pobj.type, self.type)
        self.assertEqual(pobj.name, self.name)

    def test_init_type_principal(self):
        pobj = Principal(self.name, self.type)
        self.assertEqual(pobj.type, self.type)
        self.assertEqual(pobj.name, self.name)

    def test_parse(self):
        pobj = Principal()
        pobj.parse(self.principal)
        self.assertEqual(pobj.type, self.type)
        self.assertEqual(pobj.name, self.name)

    def test_str(self):
        pobj = Principal(self.principal)
        self.assertEqual(pobj.__str__(), self.principal)

    def test_repr_type(self):
        pobj = Principal(type=self.type)
        self.assertEqual(pobj.__repr__(), self.repr_type)

    def test_repr_name(self):
        pobj = Principal(name=self.name)
        self.assertEqual(pobj.__repr__(), self.repr_name)

    def test_repr_all(self):
        pobj = Principal(self.principal)
        self.assertEqual(pobj.__repr__(), self.repr_all)

