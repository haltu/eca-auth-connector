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
from django.http import HttpResponseRedirect
from django.template.response import TemplateResponse
from django.utils.http import is_safe_url
from django.views.decorators.cache import never_cache
from django.views.decorators.debug import sensitive_post_parameters
from django.contrib.auth import authenticate, REDIRECT_FIELD_NAME, login as auth_login
from django.contrib.sites.models import get_current_site
from selector import settings

LOG = logging.getLogger(__name__)


@sensitive_post_parameters()
@never_cache
def login(request, template_name='registration/login.html',
          redirect_field_name=REDIRECT_FIELD_NAME,
          current_app=None, extra_context=None):
    """
    Does the login by passing request.META to authbackend.
    If no identity found then shows the template.
    """
    redirect_to_request = request.REQUEST.get(redirect_field_name, '')
    redirect_to = settings.LOGIN_REDIRECT_URL

    # Ensure the user-originating redirection url is safe.
    if is_safe_url(url=redirect_to_request, host=request.get_host()):
        redirect_to = redirect_to_request
    else:
        redirect_to = settings.LOGIN_REDIRECT_URL

    print repr(request.META)

    user = authenticate(request_meta=request.META)
    if not user:
        LOG.info('Could not authenticate user from the headers')
    if user:
        # Okay, security check complete. Log the user in.
        auth_login(request, user)
        meta = {}
        # We store the auth data in the session. It can be handy in
        # other parts of the site.
        keys = [
          'HTTP_AUTHENTICATOR',
          'HTTP_AUTHNID',
          'HTTP_MPASS_OID',
          'HTTP_MPASS_GIVENNAME',
          'HTTP_MPASS_SURNAME',
          'HTTP_MPASS_GROUP',
          'HTTP_MPASS_ROLE',
          'HTTP_MPASS_SCHOOL',
          'HTTP_MPASS_MUNICIPALITY',
          'HTTP_SHIB_AUTHENTICATION_METHOD',
        ]
        for k in keys:
          meta[k] = request.META.get(k, None)
        request.session['request_meta'] = meta
        return HttpResponseRedirect(redirect_to)

    current_site = get_current_site(request)
    context = {
        redirect_field_name: redirect_to,
        'site': current_site,
        'site_name': current_site.name,
        'meta': request.META,
    }
    if extra_context is not None:
        context.update(extra_context)
    return TemplateResponse(request, template_name, context, current_app=current_app)

# vim: tabstop=2 expandtab shiftwidth=2 softtabstop=2

