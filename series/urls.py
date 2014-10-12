# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required
from series.views import SeriesView, EpisodeView, EpisodeWatchView

urlpatterns_series = patterns('',
                             url(r'^series/add$', login_required(SeriesView.as_view()), name='series_new'),
                             url(r'^series/(?P<series_id>\d+)/$', SeriesView.as_view(), name='series'),

                             url(r'^series/(?P<series_id>\d+)/ep/add', login_required(EpisodeView.as_view()),
                                 name='episode_new'),
                             url(r'^series/(?P<series_id>\d+)/ep/(?P<episode_id>\d+)/watch', EpisodeWatchView.as_view(),
                                 name='episode_watch'),
                             url(r'^series/(?P<series_id>\d+)/ep/(?P<episode_id>\d+)/', EpisodeView.as_view(),
                                 name='episode'),
                             )