# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url


urlpatterns = patterns('',
                       url(r'^sign/in$', 'member.views.sign_in'),
                       url(r'^sign/out$', 'member.views.sign_out'),
                       url(r'^sign/fb/$', 'member.views.oauth_facebook'),
                       url(r'^sign/fb/auth$', 'member.views.oauth_facebook_auth'),
                       )