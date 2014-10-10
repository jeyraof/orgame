from django.conf.urls import patterns, include, url
from django.contrib import admin
from member.urls import (urlpatterns_sign, urlpatterns_settings, urlpatterns_user)
from .views import main

urlpatterns = patterns('',
                       url(r'^$', main, name='main'),
                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^sign/', include(urlpatterns_sign)),
                       url(r'^settings/', include(urlpatterns_settings)),
                       url(r'^', include(urlpatterns_user)),
                       )
