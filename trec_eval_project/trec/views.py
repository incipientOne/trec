from django.shortcuts import render
from django.http import HttpResponse
from trec.models import Track, Task, Researcher, Run

from trec.forms import UserForm, UserProfileForm

# About FAQ page for the site
def about(request):
  context_dict = {'boldmessage': "Context Dict Message For About Page"}
  return render(request, 'trec/about.html', context_dict)


# The home / main page for the site
def home(request):
  context_dict = {'boldmessage': "Context Dict Message For Home Page"}
  return render(request, 'trec/home.html', context_dict)


# Used to register a user
def register(request):
	registered = False
	
	if request.method == 'POST':
		user_form = UserForm(data=request.POST)
		profile_form = UserProfileForm(data=request.POST)
		
		if user_form.is_valid() and profile_form.is_valid():
			user = user_form.save()
			
			user.set_password(user.password)
			user.save()
			
			profile = profile_form.save(commit=False)
			profile.user = user
			
			if 'picture' in request.FILES:
				profile.picture = request.FILES['picture']
				
			profile.save()
			
			registered = True
		
		else: 
			print user_form.errors, profile_form.errors
	
	else:
		user_form = UserForm()
		profile_form = UserProfileForm()
		
	return render(request,
			'trec/register.html',
			{'user_form':user_form, 'profile_form':profile_form, 'registered':registered})


# Runs detail
def run(request, run_title_slug):
  context_dict = {}
  
  try:
  # Get the specific track
  	task = Task.objects.get(slug=run_title_slug)
  	
  	print task
  
  # Store its title
  	context_dict['task_title'] = task.title
  
  # Get the specific tasks and store info context dict
  	runs = Run.objects.filter(task=task)	
  	context_dict['runs'] = runs
  	
  	context_dict['task'] = task
  
  except Task.DoesNotExist:
  	pass
  
  return render(request, 'trec/run.html', context_dict)


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

		

# The main tracks page
def tracks(request):
	category_list = Track.objects.order_by("title")	
	context_dict = {'boldmessage': "Context Dict Message For Tracks", 'track_list' : category_list}
	return render(request, 'trec/tracks.html', context_dict) 






































