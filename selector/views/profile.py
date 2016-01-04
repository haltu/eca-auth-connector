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
from django.core.urlresolvers import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.shortcuts import redirect
from django.views.generic import TemplateView
from django.views.generic.base import View
from django.contrib.auth.decorators import login_required
from django.contrib.auth import REDIRECT_FIELD_NAME
from selector.roledb import roledb_client, APIResponse
from selector.models import AuthAssociationToken

LOG = logging.getLogger(__name__)


class AdminLoginMixin(object):
  @method_decorator(login_required(login_url=reverse_lazy('login.admin')))
  def dispatch(self, request, *args, **kwargs):
    return super(AdminLoginMixin, self).dispatch(request, *args, **kwargs)


class ProfileView(AdminLoginMixin, TemplateView):
  template_name = 'profile.html'

  def get_context_data(self, **kwargs):
    context = super(ProfileView, self).get_context_data(**kwargs)
    try:
      user_data = roledb_client('get', 'query/{username}'.format(username=self.request.user.username))
      context['attributes'] = user_data.get('attributes', None)
    except APIResponse:
      context['attributes'] = []
    return context


class AuthAssociateView(AdminLoginMixin, View):
  """
  Auth method association flow start point. Admin login is required to identify user
  account. After admin login is finished, a registration token is created and
  the user is redirected back to the login SAML endpoint force triggering a
  new login. After completing login with a new authentication source,
  user will return with the token and a SAML attribute identifying the new source.
  The registration token is used by the login view to connect the new auth method
  to the original user account and write that attribute to auth-data service.
  """

  def get(self, request, *args, **kwargs):
    token = AuthAssociationToken.objects.create(user=request.user)
    # Shibboleth should return to login view for storing the SAML attributes to session
    # then redirect to the callback view with the token in URL
    return_url = reverse('login.admin') + '?%s=' % REDIRECT_FIELD_NAME + reverse('auth.associate.callback', kwargs={'token': token.token})
    url = reverse('login.admin') + 'Shibboleth.sso/Login?forceAuthn=True&target={return_url}'.format(return_url=return_url)
    return HttpResponseRedirect(url)


class AuthAssociateCallbackView(View):
  """
  Auth association flow callback. After completing new login in Auth Proxy,
  user will return with the authn id SAML attribute to this view. The registration token is
  used to connect the authentication method to the original user account and write that
  attribute to auth-data service.
  """
  #template_name = 'mepin_associate_success.html'

  @method_decorator(login_required(login_url=reverse_lazy('login.admin')))
  def dispatch(self, request, *args, **kwargs):
    return super(AuthAssociateCallbackView, self).dispatch(request, *args, **kwargs)

  def get(self, request, *args, **kwargs):
    token = request.kwargs.get('token', None)
    # user is returning from Auth Proxy with the token we generated and the new
    # authentication method as a SAML attribute
    try:
      active_token = AuthAssociationToken.objects.get(token=token, is_used=False)
    except AuthAssociationToken.DoesNotExist:
      #TODO: error page
      raise Http404
    auth_method_name = request.session['request_meta'].get('HTTP_MPASS_AUTHENTICATOR', None)
    if not auth_method_name:
      LOG.error('Authentication association attempted but authentication method missing', extra={'data': {'meta': request.session['request_meta'], 'user': request.user.username}})
      return HttpResponse('Authentication method missing', status=400)
    authn_id = request.session['request_meta'].get('HTTP_MPASS_AUTHNID', None)
    if not authn_id:
      LOG.error('Authentication association attempted but authentication id missing', extra={'data': {'meta': request.session['request_meta'], 'user': request.user.username}})
      return HttpResponse('Authentication id missing', status=400)

    # Associate new authentication method to the active user account and redirect
    # back to the profile view
    active_token.associate(auth_method_name, authn_id)
    return redirect('profile')



# vim: tabstop=2 expandtab shiftwidth=2 softtabstop=2

