from django.conf.urls import patterns, include, url
from django.contrib import admin
from member.urls import (urlpatterns_sign, urlpatterns_settings, urlpatterns_user)
from orgame.views import IndexView, SearchView
from series.urls import (urlpatterns_series)

urlpatterns = patterns('',
                       url(r'^$', IndexView.as_view(), name='main'),
                       url(r'^search', SearchView.as_view(), name='search'),
                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^sign/', include(urlpatterns_sign)),
                       url(r'^settings/', include(urlpatterns_settings)),
                       url(r'^', include(urlpatterns_user)),
                       url(r'^', include(urlpatterns_series)),
                       )
