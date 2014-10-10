# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required
from django.views.generic.base import RedirectView
from member.views import SettingsView, UserView


urlpatterns_sign = patterns('',
                            url(r'^$', RedirectView.as_view(pattern_name='signin', permanent=False)),
                            url(r'^in$', 'member.views.sign_in', name='signin'),
                            url(r'^out$', 'member.views.sign_out', name='signout'),
                            url(r'^fb/$', 'member.views.oauth_facebook', name='facebook'),
                            url(r'^fb/auth$', 'member.views.oauth_facebook_auth', name='facebook_oauth'),
                            )

urlpatterns_settings = patterns('',
                                url(r'^$', login_required(SettingsView.as_view()), name='settings'),
                                )

urlpatterns_user = patterns('',
                            url(r'collection/$', UserView.as_view(), name='my_collection'),
                            url(r'^user/(?P<nickname>[a-zA-Z0-9_-]*)$', UserView.as_view(), name='user_collection'),
                            )