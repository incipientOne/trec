from django.conf.urls import patterns, url
from trec import views

urlpatterns = patterns('',
        url(r'^$', views.home, name='home'),
        url(r'^about', views.about, name='about'),
        url(r'^tracks', views.tracks, name='tracks'),
        url(r'^task/(?P<task_title_slug>[\w\-]+)/$', views.task, name='task'),							# Task slug urls for tasks within a track
        url(r'^run/(?P<run_title_slug>[\w\-]+)/$', views.run, name='run'),								# Run slug url for all runs within a task
        url(r'^run_detail/(?P<run_detail_slug>[\w\-]+)/$', views.run_detail, name='run_detail'),		# Run detail url for details of specific runs within a task
        url(r'^register/$', views.register, name='register'),
        url(r'^profile/', views.profile, name='profile'),
        )
