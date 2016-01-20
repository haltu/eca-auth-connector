
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

import mock
from django.test import TestCase
from selector.tests import factories as f


class TestAttributeAPIView(TestCase):

  def setUp(self):
    self.user = f.UserFactory(username='foo', password='bar')
    self.client.login(username='foo', password='bar')
    self.url = u'/api/1/me/attributes'

  def test_get(self):
    response = self.client.get(self.url)
    self.assertEqual(response.status_code, 405)

  @mock.patch('selector.views.api.roledb_client')
  def test_post_invalid_action(self, roledb_mock):
    data = {'action': 'invalid', 'name': 'name', 'value': 'value'}
    response = self.client.post(self.url, data=data)
    self.assertEqual(response.status_code, 400)
    self.assertFalse(roledb_mock.called)

  @mock.patch('selector.views.api.roledb_client')
  def test_post_add_action(self, roledb_mock):
    data = {'action': 'add', 'name': 'name', 'value': 'value'}
    response = self.client.post(self.url, data=data)
    self.assertEqual(response.status_code, 400)
    self.assertFalse(roledb_mock.called)

  @mock.patch('selector.views.api.roledb_client')
  def test_post_delete_action_name_is_none(self, roledb_mock):
    data = {'action': 'delete'}
    response = self.client.post(self.url, data=data)
    self.assertEqual(response.status_code, 400)
    self.assertFalse(roledb_mock.called)

  @mock.patch('selector.views.api.paged_query')
  @mock.patch('selector.views.api.roledb_client')
  def test_post_delete_action_404(self, roledb_mock, query_mock):
    data = {'action': 'delete', 'name': 'foo'}
    query_mock.return_value = []
    response = self.client.post(self.url, data=data)
    self.assertEqual(response.status_code, 404)
    self.assertFalse(roledb_mock.called)

  @mock.patch('selector.views.api.paged_query')
  @mock.patch('selector.views.api.roledb_client')
  def test_post_delete_action_500(self, roledb_mock, query_mock):
    data = {'action': 'delete', 'name': 'foo'}
    query_mock.return_value = ['first', 'second']
    response = self.client.post(self.url, data=data)
    self.assertEqual(response.status_code, 500)
    self.assertFalse(roledb_mock.called)

  @mock.patch('selector.views.api.paged_query')
  @mock.patch('selector.views.api.roledb_client')
  def test_post_delete_action(self, roledb_mock, query_mock):
    data = {'action': 'delete', 'name': 'foo'}
    query_mock.return_value = [{'id': 123}]
    response = self.client.post(self.url, data=data)
    self.assertEqual(response.status_code, 200)
    self.assertTrue(roledb_mock.called)
    roledb_mock.assert_called_once_with('delete', 'userattribute/123')

# vim: tabstop=2 expandtab shiftwidth=2 softtabstop=2

