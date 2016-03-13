from django.conf.urls import patterns, url
from trec import views

urlpatterns = patterns('',
        url(r'^$', views.home, name='home'),
        url(r'^about', views.about, name='about'),
        url(r'^tracks', views.tracks, name='tracks'),
        url(r'^task/(?P<task_title_slug>[\w\-]+)/$', views.task, name='task'),
        )
