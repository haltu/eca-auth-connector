
from django.conf.urls import patterns, include, url
from django.contrib import admin

from selector.views import UserView, AdminView, login

urlpatterns = patterns('',
    url(r'^admin$', AdminView.as_view()),
    url(r'^user$', UserView.as_view()),
    url(r'^saml/admin$', login),
    url(r'^saml/user$', login),
    url(r'^admin/', include(admin.site.urls)),
)

