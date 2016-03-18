from django.shortcuts import render
from django.http import HttpResponse
from trec.models import Track, Task, Researcher, Run, User, Recall_val, P_value, Run_type, Query_type, Feedback_type

from trec.forms import UserForm, UserProfileForm, EditUserInfoForm, AddRun

from populate_trec import add_researcher, add_run

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

    # Get the required info from the user and add as new researcher to database
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

            add_researcher(user, user)					# Add as researcher to db

        else:
            print user_form.errors, profile_form.errors

    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render(request,
                  'trec/register.html',
                  {'user_form': user_form, 'profile_form': profile_form, 'registered': registered})


# All runs for a given task
def run(request, run_title_slug):
    context_dict = {}

    try:
        # Get the specific task
        task = Task.objects.get(slug=run_title_slug)

        # Store its title
        context_dict['task_title'] = task.title

        # Get the runs within that task and store into context dict along with task itself
        runs = Run.objects.filter(task=task)
        context_dict['runs'] = runs

        context_dict['task'] = task

    except Task.DoesNotExist:
        pass

    return render(request, 'trec/run.html', context_dict)


# One specific run's details page
def run_detail(request, run_detail_slug):
    context_dict = {}

    try:
        # Get the specific run and store in context-dict: including all scores for graphs
        run = Run.objects.get(slug=run_detail_slug)
        context_dict['run'] = run
        context_dict['researcher'] = run.researcher
        recalls = Recall_val.objects.filter(run=run)
        recall_data = []
        for r in recalls:
            recall_data.append([r.recall_number, r.score])
        recall_data = [['Recall', 'Precision']] + sorted(recall_data, key=lambda i:i[0])
        context_dict['recall_data'] = recall_data


        p_vals = P_value.objects.filter(run=run)
        p_data = []
        for p in p_vals:
            p_data.append([p.p_number, p.score])
        p_data = [['Number of Documents', 'Precision']] + sorted(p_data, key=lambda i:i[0])
        context_dict['p_data'] = p_data

    except Run.DoesNotExist:
        pass

    return render(request, 'trec/run_detail.html', context_dict)


# Task view to display all the tasks within a track
def task(request, task_title_slug):
    context_dict = {}

    try:
        # Get the specific track
        track = Track.objects.get(slug=task_title_slug)

        # Store its title
        context_dict['task_title'] = track.title

        # Get the tasks and store info context dict
        tasks = Task.objects.filter(track=track)
        context_dict['tasks'] = tasks

        context_dict['task'] = track

    except Track.DoesNotExist:
        pass

    return render(request, 'trec/task.html', context_dict)


# The main tracks page - get all the tracks ordered alphabetically
def tracks(request):
    category_list = Track.objects.order_by("title")
    context_dict = {'boldmessage': "Context Dict Message For Tracks", 'track_list': category_list}
    return render(request, 'trec/tracks.html', context_dict)

   
# User profile view for non-logged in users wishing to view
# the profile details of a user who has uploaded a run
def user_profile(request, researcher_detail_slug):
	
	context_dict = {}
	user = User.objects.get(username=researcher_detail_slug)
	research = Researcher.objects.get(user=user)
	context_dict["researcher"] = research

	return render(request, "trec/user_profile.html", context_dict)

    
# Requires user log in 
# Handles user profile editing by fetching researcher data and altering the database
def add_run(request, task_slug):
    context_dict = {}
    username = request.user
    user = User.objects.get(username=username)
    research = Researcher.objects.get(user=user)
    task = Task.objects.get(slug=task_slug)
    run_id = len(Run.objects.all()) + 1

    # Get the info via the edit user form and update the researcher in question
    if request.method == 'POST':
        profile_form = AddRun(data=request.POST)

        if profile_form.is_valid():
            profile = profile_form.save(commit=False)
            
            # Handle profile picture change - test this as unsure if working
            
            profile.result_file = request.FILES['result_file']
            
            add_run(research, task, profile.name, profile.description, profile.result_file_path, Run_type.AUTOMATIC, Query_type.OTHER, Feedback_type.NONE,
            run_id)
            
            print "run added"      
        else:
            print profile_form.errors
        
    else:
        profile_form = AddRun(instance=request.user)

    context_dict['profile_form'] = profile_form
    context_dict['researcher'] = research
    
    return render(request, "trec/add_run.html", context_dict) 
    
# Requires user log in 
# Handles user profile editing by fetching researcher data and altering the database
def edit_profile(request):
    context_dict = {}
    username = request.user
    user = User.objects.get(username=username)
    research = Researcher.objects.get(user=user)
    context_dict['edit'] = True
    
    # Get the info via the edit user form and update the researcher in question
    if request.method == 'POST':
        profile_form = EditUserInfoForm(data=request.POST)

        if profile_form.is_valid():
            profile = profile_form.save(commit=False)
            
            # Handle profile picture change - test this as unsure if working
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']
                research.profile_picture = profile.picture
            
            # Update other categories before saving to db and returning
            research.display_name = profile.display_name
            research.website = profile.website
            research.organisation = profile.organisation
            research.save()

            context_dict['edit'] = False
            
        else:
            print profile_form.errors
        
    else:
        profile_form = UserProfileForm(instance=request.user)

    context_dict['profile_form'] = profile_form
    context_dict['researcher'] = research
    
    
    return render(request, "trec/profile.html", context_dict)

def profile(request):
    username = request.user
    user = User.objects.get(username=username)
    context_dict = {}
    context_dict['researcher'] = Researcher.objects.get(user=user)
    
    return render(request, "trec/profile.html", context_dict)    