
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
from django.contrib.auth.models import Permission
from django.test import TestCase
from selector.tests import factories as f


@mock.patch('selector.views.invitator.paged_query')
class TestSearchView(TestCase):

  def setUp(self):
    self.user = f.UserFactory(username='foo', password='bar')
    self.client.login(username='foo', password='bar')
    self.url = u'/search'

  def test_get_not_admin(self, query_mock):
    response = self.client.get(self.url)
    self.assertRedirects(response, expected_url='permission?next=/search')
    self.assertFalse(query_mock.called)

  def test_get_has_permission(self, query_mock):
    perm = Permission.objects.get(codename='can_invite')
    self.user.user_permissions.add(perm)
    response = self.client.get(self.url)
    self.assertContains(response, 'html')
    self.assertFalse(query_mock.called)

  def test_post_form(self, query_mock):
    perm = Permission.objects.get(codename='can_invite')
    self.user.user_permissions.add(perm)
    query_mock.return_value = [{'username': 'foo'}, {'username': 'bar'}]
    data = {'municipality': 'muni1', 'school': 'school1', 'group': 'group1'}
    response = self.client.post(self.url, data=data)
    self.assertTrue(response.render())
    self.assertEqual(response.status_code, 200)
    self.assertTrue(query_mock.called)
    self.assertIn('inviteform_users_choices', dict(self.client.session))


class TestInviteView(TestCase):

  def setUp(self):
    perm = Permission.objects.get(codename='can_invite')
    self.user = f.UserFactory(username='foo', password='bar')
    self.user.user_permissions.add(perm)
    self.client.login(username='foo', password='bar')
    self.url = u'/invite'

  def test_get(self):
    response = self.client.get(self.url)
    self.assertContains(response, 'html')
    self.assertTemplateUsed(response, 'invite.html')
    self.assertTemplateUsed(response, 'forms/inviteform_user.html')

  def test_post(self):
    u = f.UserFactory()
    s = self.client.session
    s['inviteform_users_choices'] = [(u.username, {'username': u.username})]
    s['request_meta'] = {'HTTP_MPASS_OID': 'oid_mock',
        'HTTP_SHIB_AUTHENTICATION_METHOD': 'mockmethod'}
    s.save()
    data = {'users': u.username}
    response = self.client.post(self.url, data=data)
    self.assertContains(response, 'html')
    self.assertTemplateUsed(response, 'invited.html')


class TestDebugView(TestCase):

  def setUp(self):
    perm = Permission.objects.get(codename='can_invite')
    self.user = f.UserFactory(username='foo', password='bar')
    self.user.user_permissions.add(perm)
    self.client.login(username='foo', password='bar')
    self.url = u'/debug'

  def test_get(self):
    u = f.UserFactory()
    s = self.client.session
    s['inviteform_users_choices'] = [(u.username, {'username': u.username})]
    s['request_meta'] = {'HTTP_MPASS_OID': 'oid_mock',
        'HTTP_SHIB_AUTHENTICATION_METHOD': 'mockmethod'}
    s.save()
    response = self.client.get(self.url)
    self.assertContains(response, 'html')
    self.assertTemplateUsed(response, 'debug.html')
    self.assertTemplateUsed(response, 'base_info.html')
    self.assertTemplateUsed(response, 'base.html')


# vim: tabstop=2 expandtab shiftwidth=2 softtabstop=2

