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
from selector.roledb import roledb_client

LOG = logging.getLogger(__name__)


class UserLoginMixin(object):
  @method_decorator(login_required(login_url=reverse_lazy('register.user')))
  def dispatch(self, request, *args, **kwargs):
    return super(UserLoginMixin, self).dispatch(request, *args, **kwargs)


class ProfileView(UserLoginMixin, TemplateView):
  template_name = 'profile.html'

  def get_context_data(self, **kwargs):
    context = super(ProfileView, self).get_context_data(**kwargs)
    user_data = roledb_client('get', 'query/{username}'.format(username=self.request.user.username))
    context['attributes'] = user_data.get('attributes', None)
    return context


# vim: tabstop=2 expandtab shiftwidth=2 softtabstop=2

