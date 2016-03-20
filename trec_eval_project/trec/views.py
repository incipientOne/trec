import subprocess

from django.core.exceptions import ValidationError
from django.forms.utils import ErrorList
from django.shortcuts import render, redirect
from django.http import HttpResponse
from trec.models import Track, Task, Researcher, Run, User, Recall_val, P_value, Run_type, Query_type, Feedback_type

from trec.forms import UserForm, UserProfileForm, EditUserInfoForm, AddRun

import populate_trec

# Used to get random index
from random import randrange


# About FAQ page for the site
def about(request):
    context_dict = {'boldmessage': "Context Dict Message For About Page"}
    return render(request, 'trec/about.html', context_dict)


# The home / main page for the site
def home(request):
    run_list = Run.objects.all()
    rand_num = randrange(0, len(run_list))

    context_dict = {'random_run': run_list[rand_num]}
    return render(request, 'trec/home.html', context_dict)
    

def users(request):
	return render(request, 'trec/users.html', {'users': Researcher.objects.all()})

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
            # Add as researcher to db
            populate_trec.add_researcher(user, user)

        else:
            print user_form.errors, profile_form.errors

    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render(request,
                  'trec/register.html',
                  {'user_form': user_form, 'profile_form': profile_form, 'registered': registered})


# All runs for a given task
def task(request, task_slug):
    context_dict = {}

    try:
        # Get the specific task
        task = Task.objects.get(slug=task_slug)

        # Get the runs within that task and store into context dict along with task itself
        runs = Run.objects.filter(task=task)
        context_dict['runs'] = runs
        context_dict['task'] = task

        map_vals = [['', 'MAP Score']]
        for run in runs:
            map_vals.append([str(run.name), run.map_val])

        context_dict['map_vals'] = map_vals

    except Task.DoesNotExist:
        pass

    return render(request, 'trec/task.html', context_dict)


# One specific run's details page
def run(request, run_slug):
    context_dict = {}

    try:
        # Get the specific run and store in context-dict: including all scores for graphs
        run = Run.objects.get(slug=run_slug)
        context_dict['run'] = run
        context_dict['researcher'] = run.researcher
        recalls = Recall_val.objects.filter(run=run)
        recall_data = []
        for r in recalls:
            recall_data.append([r.recall_number, r.score])
        recall_data = [['Recall', 'Precision']] + sorted(recall_data, key=lambda i: i[0])
        context_dict['recall_data'] = recall_data

        p_vals = P_value.objects.filter(run=run)
        p_data = []
        for p in p_vals:
            p_data.append([p.p_number, p.score])
        p_data = [['Number of Documents', 'Precision']] + sorted(p_data, key=lambda i: i[0])
        context_dict['p_data'] = p_data

    except Run.DoesNotExist:
        pass

    return render(request, 'trec/run.html', context_dict)


# Task view to display all the tasks within a track
def track(request, track_slug):
    context_dict = {}

    try:
        # Get the specific track
        track = Track.objects.get(slug=track_slug)

        # Get the tasks and store info context dict
        tasks = Task.objects.filter(track=track)
        context_dict['tasks'] = tasks
        context_dict['track'] = track

        task_average = [['', 'Average MAP Score:']]

        for task in tasks:
            average = 0
            runs = Run.objects.filter(task=task)
            for run in runs:
                average += run.map_val
            average = average / len(runs)
            task_average.append([str(task.title), average])

        context_dict['task_average'] = task_average

    except Track.DoesNotExist:
        pass

    return render(request, 'trec/track.html', context_dict)


# The main tracks page - get all the tracks ordered alphabetically
def tracks_list(request):
    category_list = Track.objects.order_by("title")
    context_dict = {'track_list': category_list}

    track_average = [['', 'Average Track MAP']]

    for track in category_list:
        average = 0
        final = 0
        tasks = Task.objects.filter(track=track)
        for task in tasks:
            runs = Run.objects.filter(task=task)
            for run in runs:
                average = average + run.map_val
            average = average / len(runs)
            final = final + average
        final = final / len(tasks)
        track_average.append([str(track.title), final])

    context_dict['track_average'] = track_average

    return render(request, 'trec/tracks_list.html', context_dict)


# User profile view for non-logged in users wishing to view
# the profile details of a user who has uploaded a run
def user(request, researcher_detail_slug):
    context_dict = {}
    user = User.objects.get(username=researcher_detail_slug)
    research = Researcher.objects.get(user=user)
    context_dict["researcher"] = research
    context_dict["runs"] = Run.objects.filter(researcher=research)

    return render(request, "trec/user_profile.html", context_dict)


# Requires user log in 
# Handles adding a new run to a task.
def add_run(request, task_slug):
    context_dict = {}
    username = request.user
    user = User.objects.get(username=username)
    researcher = Researcher.objects.get(user=user)
    task = Task.objects.get(slug=task_slug)
    run_id = len(Run.objects.all()) + 1

    # Get the info via the AddRun form and create a new run.
    if request.method == 'POST':
        profile_form = AddRun(request.POST, request.FILES)
        # profile_form = UploadFileForm(request.POST, request.FILES)
        if profile_form.is_valid():
            profile = profile_form.save(commit=False)
            profile.task = task
            profile.researcher = researcher
            profile.run_id = run_id

            # we save this before calling trec_eval, as trec_eval needs the files to be stored in the file system.
            profile.save();

            try:
                # attempt to calculate stats with trec_eval.
                profile.populate_with_trec_eval_data()
                profile.save();

            except subprocess.CalledProcessError:
                # add error message for user.
                profile_form._errors['result_file'] = ErrorList(["Could not process run file."])
                # clean up the attempt to add a run.
                profile.delete()
    else:
        profile_form = AddRun(instance=request.user)

    context_dict['profile_form'] = profile_form
    context_dict['task'] = task

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
        profile_form = EditUserInfoForm(request.POST, request.FILES)

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

            return redirect('profile')

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
    research = Researcher.objects.get(user=user)
    context_dict = {}
    context_dict['researcher'] = research
    context_dict["runs"] = Run.objects.filter(researcher=research)
    return render(request, "trec/profile.html", context_dict)
