# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required
from django.views.generic.base import RedirectView
from member.views import SettingsView


urlpatterns_sign = patterns('',
                            url(r'^$', RedirectView.as_view(pattern_name='member.views.sign_in', permanent=False)),
                            url(r'^in$', 'member.views.sign_in', name='signin'),
                            url(r'^out$', 'member.views.sign_out', name='signout'),
                            url(r'^fb/$', 'member.views.oauth_facebook', name='facebook'),
                            url(r'^fb/auth$', 'member.views.oauth_facebook_auth', name='facebook_oauth'),
                            )

urlpatterns_settings = patterns('',
                                url(r'^$', login_required(SettingsView.as_view()), name='settings'),
                                )
