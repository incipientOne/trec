from django.shortcuts import render
from django.http import HttpResponse
from trec.models import Track, Task, Researcher, Run

# About FAQ page for the site
def about(request):
  context_dict = {'boldmessage': "Context Dict Message For About Page"}
  return render(request, 'trec/about.html', context_dict)


# One specific task
def task(request, task_title_slug):
  context_dict = {}
  
  try:
  # Get the specific track
  	track = Track.objects.get(slug=task_title_slug)
  
  # Store its title
  	context_dict['task_title'] = track.title
  
  # Get the specific tasks and store info context dict
  	tasks = Task.objects.filter(track=track)	
  	context_dict['tasks'] = tasks
  	
  	context_dict['task'] = track
  
  except Track.DoesNotExist:
  	pass
  
  return render(request, 'trec/task.html', context_dict)


# The home / main page for the site
def home(request):
  context_dict = {'boldmessage': "Context Dict Message For Home Page"}
  return render(request, 'trec/home.html', context_dict)
  

# The main tracks page
def tracks(request):
	category_list = Track.objects.order_by("title")	
	context_dict = {'boldmessage': "Context Dict Message For Tracks", 'track_list' : category_list}
	return render(request, 'trec/tracks.html', context_dict) 
