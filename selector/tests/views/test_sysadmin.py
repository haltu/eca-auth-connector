
# -*- coding: utf-8 -*-

# The MIT License (MIT)
#
# Copyright (c) 2015 Haltu Oy, http://haltu.fi
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
# pylint: disable=locally-disabled, no-member

from django.test import TestCase
from selector.tests import factories as f


class TestSysadmin(TestCase):

  def setUp(self):
    self.user = f.UserFactory(username='foo', password='bar')
    self.user.is_staff = True
    self.user.is_superuser = True
    self.user.save()
    self.client.login(username='foo', password='bar')
    self.url = u'/sysadmin/'

  def test_get(self):
    response = self.client.get(self.url)
    self.assertEqual(response.status_code, 200)


# vim: tabstop=2 expandtab shiftwidth=2 softtabstop=2

