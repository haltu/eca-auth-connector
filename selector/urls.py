
from django.conf.urls import patterns, include, url
from django.contrib import admin
from selector.forms import AuthenticationForm

admin.site.login_form = AuthenticationForm

from selector.views import InvitatorView, InviteeView, IndexView, SearchView, login

urlpatterns = patterns('',
    url(r'^$', IndexView.as_view()),
    url(r'^search$', SearchView.as_view()),
    url(r'^invitator$', InvitatorView.as_view()),
    url(r'^invitee$', InviteeView.as_view()),
    url(r'^saml/admin/$', login),
    url(r'^saml/user/$', login),
    url(r'^sysadmin/', include(admin.site.urls)),
)

