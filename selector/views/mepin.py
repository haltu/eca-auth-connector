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


import logging
from django.core.urlresolvers import reverse_lazy, reverse
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from django.views.generic.base import View
from django.contrib.auth.decorators import login_required
from selector.models import AuthAssociationToken

LOG = logging.getLogger(__name__)


class MePinInfoView(TemplateView):
  """
  Display informational page about MePin registration with a button for starting
  registration process. Button takes the user to RegisterMePinView
  """
  template_name = 'mepin_info.html'


class MePinAssociateView(View):
  """
  MePin registration flow start point. Admin login is required to identify user
  account. After admin login is finished, a registration token is created and
  the user is redirected to the /saml/mepin SAML endpoint triggering a login
  with the MePin IdP. After completing login and/or registration in MePin,
  user will return with a MePin id SAML attribute. The registration token is
  used to connect the MePin id to the original user account and write that
  attribute to auth-data service.
  """

  @method_decorator(login_required(login_url=reverse_lazy('login.admin')))
  def dispatch(self, request, *args, **kwargs):
    return super(MePinAssociateView, self).dispatch(request, *args, **kwargs)

  def get(self, request, *args, **kwargs):
    # TODO: Check if user already has a mepin id associated?
    # user has come without a token - start flow by generating a token
    token = AuthAssociationToken.objects.create(user=request.user)
    return_url = reverse('mepin.callback') + '?token=' + token.token
    # url = '/saml/mepin/Shibboleth.sso/Login?forceAuthn=true&target={return_url}'.format(return_url=urlquote(return_url))
    # urlquote is disabled because Shibboleth or MePin idp does not seem to properly decode the target url
    url = reverse('mepin.callback') + 'Shibboleth.sso/Login?forceAuthn=true&target={return_url}'.format(return_url=return_url)
    return HttpResponseRedirect(url)


class MePinAssociateCallbackView(TemplateView):
  """
  MePin registration flow end point. After completing login and/or registration in MePin,
  user will return with a MePin id SAML attribute to this view. The registration token is
  used to connect the MePin id to the original user account and write that
  attribute to auth-data service.
  """
  template_name = 'mepin_associate_success.html'

  @method_decorator(login_required(login_url=reverse_lazy('login.admin')))
  def dispatch(self, request, *args, **kwargs):
    return super(MePinAssociateCallbackView, self).dispatch(request, *args, **kwargs)

  def get(self, request, *args, **kwargs):
    token = request.GET.get('token', None)
    if not token:
      # user has come without a token - start flow by generating a token
      token = AuthAssociationToken.objects.create(user=request.user)
      return_url = reverse('mepin.callback') + '?token=' + token.token
      # url = '/saml/mepin/Shibboleth.sso/Login?forceAuthn=true&target={return_url}'.format(return_url=urlquote(return_url))
      # urlquote is disabled because Shibboleth or MePin idp does not seem to properly decode the target url
      url = reverse('mepin.callback') + 'Shibboleth.sso/Login?forceAuthn=true&target={return_url}'.format(return_url=return_url)
      return HttpResponseRedirect(url)
    else:
      # user is returning from MePin IdP with the token we generated and the mepin
      # id as a SAML attribute
      try:
        active_token = AuthAssociationToken.objects.get(token=token, is_used=False)
      except AuthAssociationToken.DoesNotExist:
        # TODO: error page
        raise Http404
      # TODO: Check MePin SAML Attribute name
      mepin_id = request.META.get('HTTP_MEPIN_ID', None)
      if not mepin_id:
        # TODO: error page
        return HttpResponse('Missing Mepin ID', status=400)
      active_token.associate(request.user, 'mepin', mepin_id)
      # MePin id successfully associated, render success page
      return super(MePinAssociateCallbackView, self).get(request, *args, **kwargs)

# vim: tabstop=2 expandtab shiftwidth=2 softtabstop=2

