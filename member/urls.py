# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url
from django.views.generic.base import RedirectView


urlpatterns_sign = patterns('',
                            url(r'^$', RedirectView.as_view(pattern_name='member.views.sign_in', permanent=False)),
                            url(r'^in$', 'member.views.sign_in'),
                            url(r'^out$', 'member.views.sign_out'),
                            url(r'^fb/$', 'member.views.oauth_facebook'),
                            url(r'^fb/auth$', 'member.views.oauth_facebook_auth'),
                            )
