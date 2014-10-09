from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^dismiss/$', 'zenaida.contrib.hints.views.dismiss'),
)
