from django.shortcuts import render
from django.http import HttpResponse
from trec.models import Track

# About FAQ page for the site
def about(request):
  context_dict = {'boldmessage': "Context Dict Message For About Page"}
  return render(request, 'trec/about.html', context_dict)


# The home / main page for the site
def home(request):
  context_dict = {'boldmessage': "Context Dict Message For Home Page"}
  return render(request, 'trec/home.html', context_dict)
  

# The main tracks page
def tracks(request):
	category_list = Track.objects.order_by("title")	
	context_dict = {'boldmessage': "Context Dict Message For Tracks", 'track_list' : category_list}
	return render(request, 'trec/tracks.html', context_dict) 
