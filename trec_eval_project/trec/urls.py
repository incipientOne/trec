from django.conf.urls import patterns, url
from trec import views

urlpatterns = patterns('',
	url(r'^$', views.home, name='home'),
	url(r'^about', views.about, name='about'),

	url(r'^tracks', views.tracks_list, name='tracks'),
	url(r'^track/(?P<track_slug>[\w\-]+)/$', views.track, name='track'),										# Task slug urls for tasks within a track		
	url(r'^task/(?P<task_slug>[\w\-]+)/$', views.task, name='task'),											# Run slug url for all runs within a task
	url(r'^run/(?P<run_slug>[\w\-]+)/$', views.run, name='run'),												# Run detail url for details of specific runs within a task
	
	url(r'^add_run/(?P<task_slug>[\w\-]+)/$', views.add_run, name='add_run'),									# For users to add a run for a task
	url(r'^add_run/', views.add_run, name='add_run'),

	url(r'^users/', views.users, name='users'),																	# Master list of all users
	url(r'^user/(?P<researcher_detail_slug>[\w\-]+)/$', views.user, name='user'),		# Run detail url for details of specific runs within a task
	
	url(r'^register/$', views.register, name='register'),														# To register new users
	url(r'^profile/edit', views.edit_profile, name='edit_profile'),		
	url(r'^profile/', views.profile, name='profile'),															# For users to edit their profile details
)
