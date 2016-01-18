
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
# pylint: disable=locally-disabled, no-member, unused-argument, no-init, old-style-class, too-few-public-methods, unnecessary-lambda


import string
import factory
import factory.fuzzy
from selector import models


class UserFactory(factory.django.DjangoModelFactory):
  class Meta:
    model = models.User

  first_name = factory.Sequence(lambda n: 'First{0}'.format(n))
  last_name = factory.Sequence(lambda n: 'Last{0}'.format(n))
  email = factory.LazyAttribute(lambda u:
      '{0}.{1}@example.com'.format(u.first_name, u.last_name))
  username = factory.fuzzy.FuzzyText(length=11, chars=string.digits, prefix='1.2.246.562.24.')


class RegisterTokenFactory(factory.django.DjangoModelFactory):
  class Meta:
    model = models.RegisterToken

  user = factory.SubFactory(UserFactory)


class AuthAssociationTokenFactory(factory.django.DjangoModelFactory):
  class Meta:
    model = models.AuthAssociationToken

  user = factory.SubFactory(UserFactory)

# vim: tabstop=2 expandtab shiftwidth=2 softtabstop=2

