# -*- encoding: utf-8 -*-

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
#


import logging
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse_lazy
from django.utils.encoding import force_text
from django.utils.decorators import method_decorator
from django.views.generic import View, TemplateView, FormView
from django.contrib.auth.decorators import login_required
from django.contrib.sites.models import get_current_site
from selector.models import RegisterToken
from selector.forms import RegisterForm
from selector.roledb import paged_query, roledb_client

LOG = logging.getLogger(__name__)


class UserLoginMixin(object):
  @method_decorator(login_required(login_url=reverse_lazy('register.user')))
  def dispatch(self, request, *args, **kwargs):
    return super(UserLoginMixin, self).dispatch(request, *args, **kwargs)


class AttributeAPIView(UserLoginMixin, View):
  def post(self, request, *args, **kwargs):
    action = self.request.POST.get('action', None)
    name = self.request.POST.get('name', None)
    value = self.request.POST.get('value', None)
    user = self.request.user

    if action == 'delete':
      if name is None:
        return HttpResponse('Invalid request', status=400)
      r = list(paged_query('get', 'userattribute', params={'user': user.username, 'attribute': name}))
      if len(r) > 1:
        LOG.error('User has duplicate attributes', extra={'data': {'user': user.username, 'attribute': name}})
        return HttpResponse('Multiple attributes error', status=500)
      elif len(r) == 0:
        return HttpResponse(status=404)
      attribute_id = r[0]['id']
      roledb_client('delete', 'userattribute/{id}'.format(id=attribute_id))
      return HttpResponse('OK')
    if action == 'add':
      # get attribute
      # if not existing, create new attribute
      # add attribute with value
      # TODO: auth-data sets UserAttributes always for request.user
      pass
    else:
      return HttpResponse('Invalid action', status=400)

# vim: tabstop=2 expandtab shiftwidth=2 softtabstop=2

