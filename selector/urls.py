
from django.conf.urls import patterns, include, url
from django.contrib import admin
from selector.forms import AuthenticationForm

admin.site.login_form = AuthenticationForm

from selector.views.base import IndexView, PermissionView
from selector.views.invitator import SearchView, InviteView
from selector.views.invitator import DebugView
from selector.views.invitee import RegisterTokenView, RegisterUserView, RegisterSuccessView, RegisterFailedView
from selector.views.login import login

urlpatterns = patterns('',
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^search$', SearchView.as_view(), name='search'),
    url(r'^invite$', InviteView.as_view(), name='invite'),
    url(r'^register$', RegisterTokenView.as_view(), name='register'),
    url(r'^register/success$', RegisterSuccessView.as_view(), name='register.success'),
    url(r'^register/failed$', RegisterFailedView.as_view(), name='register.failed'),
    url(r'^register/(?P<token>.*)$', RegisterTokenView.as_view(), name='register.token'),
    url(r'^permission$', PermissionView.as_view(), name='permission'),
    url(r'^debug$', DebugView.as_view()),
    url(r'^saml/admin/$', login, name='login.admin'),
    url(r'^saml/user/$', RegisterUserView.as_view(), name='register.user'),
    url(r'^sysadmin/', include(admin.site.urls)),
)

