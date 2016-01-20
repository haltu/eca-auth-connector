
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

import mock
from django.test import TestCase
import selector.models
import selector.authbackend
from selector.tests import factories as f


class TestShibbolethBackend(TestCase):

  def setUp(self):
    self.obj = selector.authbackend.ShibbolethBackend()

  def test_authenticate_no_request_meta(self):
    credentials = {}
    res = self.obj.authenticate(**credentials)
    self.assertEqual(res, None)

  def test_authenticate_with_empty_request_meta(self):
    meta = {}
    credentials = {'request_meta': meta}
    res = self.obj.authenticate(**credentials)
    self.assertEqual(res, None)

  def test_authenticate_with_request_meta_mpass_oid(self):
    u = f.UserFactory()
    meta = {'HTTP_MPASS_OID': u.username}
    credentials = {'request_meta': meta}
    res = self.obj.authenticate(**credentials)
    self.assertEqual(res, u)

  @mock.patch('selector.authbackend.settings')
  def test_authenticate_with_request_meta_no_user(self, settings_mock):
    settings_mock.CREATE_SAML_USER = True
    meta = {
      'HTTP_MPASS_OID': 'foo',
      'HTTP_MPASS_GIVENNAME': 'First',
      'HTTP_MPASS_SURNAME': 'Last',
    }
    credentials = {'request_meta': meta}
    self.obj.authenticate(**credentials)
    self.assertEqual(selector.models.User.objects.count(), 1)

  @mock.patch('selector.authbackend.settings')
  def test_authenticate_with_request_meta_dont_create_user(self, settings_mock):
    settings_mock.CREATE_SAML_USER = False
    meta = {
      'HTTP_MPASS_OID': 'foo',
      'HTTP_MPASS_GIVENNAME': 'First',
      'HTTP_MPASS_SURNAME': 'Last',
    }
    credentials = {'request_meta': meta}
    res = self.obj.authenticate(**credentials)
    self.assertEqual(res, None)
    self.assertEqual(selector.models.User.objects.count(), 0)

# vim: tabstop=2 expandtab shiftwidth=2 softtabstop=2

