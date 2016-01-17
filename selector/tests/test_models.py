
# -*- coding: utf-8 -*-

import unittest
from selector.models import User
from selector.tests.factories import UserFactory


class TestUser(unittest.TestCase):

  def setUp(self):
    self.u = UserFactory.create()

  def test_get_full_name(self):
    self.assertTrue(self.u.get_full_name())

  def teadDown(self):
    pass


# vim: tabstop=2 expandtab shiftwidth=2 softtabstop=2

