from django.shortcuts import render
from django.http import HttpResponse

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
	context_dict = {'boldmessage': "Context Dict Message For Track Page"}
	return render(request, 'trec/tracks.html', context_dict) 
