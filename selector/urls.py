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


from django.conf.urls import patterns, include, url
from django.contrib import admin
from selector.forms import AuthenticationForm
from selector.views.base import IndexView, PermissionView
from selector.views.invitator import SearchView, InviteView
from selector.views.invitator import DebugView
from selector.views.invitee import RegisterTokenView, RegisterUserView, RegisterSuccessView, RegisterFailedView
from selector.views.profile import ProfileView
from selector.views.mepin import MePinInfoView, MePinAssociateView, MePinAssociateCallbackView
from selector.views.api import AttributeAPIView
from selector.views.login import login

admin.site.login_form = AuthenticationForm

urlpatterns = patterns('',
  url(r'^$', IndexView.as_view(), name='index'),
  url(r'^search$', SearchView.as_view(), name='search'),
  url(r'^invite$', InviteView.as_view(), name='invite'),
  url(r'^profile$', ProfileView.as_view(), name='profile'),
  url(r'^register$', RegisterTokenView.as_view(), name='register'),
  url(r'^register/success$', RegisterSuccessView.as_view(), name='register.success'),
  url(r'^register/failed$', RegisterFailedView.as_view(), name='register.failed'),
  url(r'^register/(?P<token>.*)$', RegisterTokenView.as_view(), name='register.token'),
  url(r'^mepin$', MePinInfoView.as_view(), name='mepin.info'),
  url(r'^mepin/associate$', MePinAssociateView.as_view(), name='mepin.associate'),
  url(r'^permission$', PermissionView.as_view(), name='permission'),
  url(r'^debug$', DebugView.as_view()),
  url(r'^saml/admin/$', login, name='login.admin'),
  url(r'^saml/user/$', RegisterUserView.as_view(), name='register.user'),
  url(r'^saml/mepin/$', MePinAssociateCallbackView.as_view(), name='mepin.callback'),
  url(r'^sysadmin/', include(admin.site.urls)),
  url(r'^api/1/me/attributes', AttributeAPIView.as_view(), name='api.attributes'),
)

# vim: tabstop=2 expandtab shiftwidth=2 softtabstop=2

