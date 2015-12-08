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

LOG = logging.getLogger(__name__)


class UserLoginMixin(object):
  @method_decorator(login_required(login_url=reverse_lazy('login.user')))
  def dispatch(self, request, *args, **kwargs):
    return super(UserLoginMixin, self).dispatch(request, *args, **kwargs)


class ClearSessionMixin(object):
  def dispatch(self, request, *args, **kwargs):
    if 'registration_token' in request.session:
      del request.session['registration_token']
    return super(ClearSessionMixin, self).dispatch(request, *args, **kwargs)


class RegisterTokenView(FormView):
  template_name = 'register.html'
  success_url = reverse_lazy('register.user')
  form_class = RegisterForm

  def store_token(self, token):
    self.request.session['registration_token'] = token.token

  def form_valid(self, form):
    self.store_token(form.cleaned_data['token'])
    return super(RegisterTokenView, self).form_valid(form)

  def get(self, request, *args, **kwargs):
    if 'token' in kwargs:
      form = RegisterForm({'token': kwargs['token']})
      if form.is_valid():
        return self.form_valid(form)
    return super(RegisterTokenView, self).get(request, *args, **kwargs)


class RegisterUserView(View):
  http_method_names = ['get']
  success_url = reverse_lazy('register.success')
  failed_url = reverse_lazy('register.failed')

  def get(self, request, *args, **kwargs):
    f = RegisterForm({'token': request.session['registration_token']})
    if f.is_valid():
      print '1'
      if 'HTTP_AUTHNID' in request.META and 'HTTP_AUTHENTICATOR' in request.META:
        print '2'
        token = f.cleaned_data['token']
        invitee = {
          'eppn': request.META.get('HTTP_AUTHNID', None),
          'auth_method': request.META.get('HTTP_AUTHENTICATOR', None),
          }
        if token.register(token.user, **invitee):
          print '3'
          return HttpResponseRedirect(self.success_url)
    return HttpResponseRedirect(force_text(self.failed_url))


class RegisterSuccessView(ClearSessionMixin, TemplateView):
  template_name = 'register_success.html'


class RegisterFailedView(ClearSessionMixin, TemplateView):
  template_name = 'register_failed.html'



