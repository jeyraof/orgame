from django.conf.urls import patterns, include, url
from django.contrib import admin
from member.urls import urlpatterns_sign
from .views import main

urlpatterns = patterns('',
                       url(r'^$', main),
                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^sign/', include(urlpatterns_sign)),
                       )
