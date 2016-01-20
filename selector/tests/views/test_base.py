
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

from django.test import TestCase, RequestFactory
from selector.tests import factories as f
import selector.views.base


class TestBaseIndexView(TestCase):

  def setUp(self):
    self.factory = RequestFactory()
    self.user = f.UserFactory(username='foo', password='bar')

  def test_get_context_data(self):
    request = self.factory.get('/index')
    request.user = self.user
    view = selector.views.base.IndexView()
    view.request = request
    context = view.get_context_data()
    self.assertEqual(context['user'], self.user)
    self.assertEqual(context['meta'], request.META)
    self.assertEqual(context['meta_keys'], request.META.keys())
    response = selector.views.base.IndexView.as_view()(request)
    self.assertEqual(response.status_code, 200)
    with self.assertTemplateUsed('index.html'):
      response.render()


class TestBasePermissionView(TestCase):

  def setUp(self):
    self.factory = RequestFactory()
    self.user = f.UserFactory(username='foo', password='bar')

  def test_get_context_data(self):
    request = self.factory.get('/index')
    request.user = self.user
    response = selector.views.base.PermissionView.as_view()(request)
    self.assertEqual(response.status_code, 200)
    with self.assertTemplateUsed('permission.html'):
      response.render()

# vim: tabstop=2 expandtab shiftwidth=2 softtabstop=2

