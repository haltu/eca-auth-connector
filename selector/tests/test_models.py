
# -*- coding: utf-8 -*-

# The MIT License (MIT)
#
# Copyright (c) 2014-2015 Haltu Oy, http://haltu.fi
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

import unittest
import mock
import selector.models
from selector.tests import factories as f


class TestUser(unittest.TestCase):

  def setUp(self):
    selector.models.RegisterToken.objects.all().delete()
    self.u = f.UserFactory(
      first_name='First',
      last_name='Last',
      email='foo@test.com',
    )

  def tearDown(self):
    del self.u

  def test_get_full_name(self):
    full_name = self.u.get_full_name()
    self.assertEqual(full_name, u'First Last', full_name)

  def test_get_short_name(self):
    short_name = self.u.get_short_name()
    self.assertEqual(short_name, self.u.first_name)

  def test_email_user(self):
    with mock.patch('selector.models.send_mail') as m:
      self.u.email_user(subject='subject', message='message')
      self.assertTrue(m.called)

  def test_create_register_tokens(self):
    self.assertFalse(selector.models.RegisterToken.objects.count())
    tokens = self.u.create_register_tokens(
        issuer_auth_method='foo',
        issuer_oid='oid',
    )
    self.assertEquals(len(tokens), 1)
    self.assertEquals(selector.models.RegisterToken.objects.count(), 1)

  def test_send_register_tokens(self):
    f.RegisterTokenFactory(user=self.u, method=selector.models.RegisterToken.EMAIL)
    f.RegisterTokenFactory(user=self.u, method='unknown_method')
    with mock.patch('selector.models.send_mail') as m:
      self.u.send_register_tokens()
      self.assertTrue(m.called)


class TestRegisterToken(unittest.TestCase):

  def setUp(self):
    self.u = f.UserFactory()

  def test_register_wrong_user(self):
    register_token = f.RegisterTokenFactory()
    res = register_token.register(user=self.u)
    self.assertFalse(res)

  def test_register_user(self):
    register_token = f.RegisterTokenFactory(user=self.u)
    self.assertFalse(register_token.is_used)
    with mock.patch('selector.models.roledb_client') as m:
      res = register_token.register(
          user=self.u,
          eppn='mockeppn',
          auth_method='mockauth',
      )
      self.assertTrue(m.called)
    self.assertTrue(res)
    self.assertTrue(register_token.is_used)

  def test_unicode(self):
    register_token = f.RegisterTokenFactory(user=self.u)
    txt = unicode(register_token)
    self.assertTrue(txt)


class TestAuthAssociationToken(unittest.TestCase):

  def setUp(self):
    self.obj = f.AuthAssociationTokenFactory()

  def tearDown(self):
    del self.obj

  def test_unicode(self):
    txt = unicode(self.obj)
    self.assertTrue(txt)

  def test_save_no_token(self):
    auth_token = f.AuthAssociationTokenFactory.build(user=f.UserFactory())
    self.assertFalse(auth_token.token)
    auth_token.save()
    self.assertTrue(auth_token.token)

  def test_save_has_token(self):
    auth_token = f.AuthAssociationTokenFactory()
    self.assertTrue(auth_token.token)
    auth_token.save()
    self.assertTrue(auth_token.token)

  def test_associate(self):
    self.assertFalse(self.obj.is_used)
    with mock.patch('selector.models.roledb_client') as m:
      res = self.obj.associate(attr_name='mockattrname', attr_value='mockvalue')
      self.assertTrue(m.called)
    self.assertTrue(res)
    self.assertTrue(self.obj.is_used)

# vim: tabstop=2 expandtab shiftwidth=2 softtabstop=2

