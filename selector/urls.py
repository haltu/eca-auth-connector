
from django.conf.urls import patterns, include, url
from django.contrib import admin
from selector.forms import AuthenticationForm

admin.site.login_form = AuthenticationForm

from selector.views import InvitatorView, InviteeView, IndexView, SearchView, RegisterView, login

urlpatterns = patterns('',
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^search$', SearchView.as_view(), name='search'),
    url(r'^register$', RegisterView.as_view(), name='register'),
    url(r'^invitator$', InvitatorView.as_view()),
    url(r'^invitee$', InviteeView.as_view()),
    url(r'^saml/admin/$', login, name='login.admin'),
    url(r'^saml/user/$', login, name='login.user'),
    url(r'^sysadmin/', include(admin.site.urls)),
)

