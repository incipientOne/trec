from django.shortcuts import render
from django.http import HttpResponse
from trec.models import Track, Task, Researcher, Run, User, Recall_val, P_value

from trec.forms import UserForm, UserProfileForm, EditUserInfoForm

from populate_trec import add_researcher


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

            add_researcher(user, user)

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
        # Get the specific run and store in context-dict
        run = Run.objects.get(slug=run_detail_slug)
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


# Task view
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


# The main tracks page
def tracks(request):
    category_list = Track.objects.order_by("title")
    context_dict = {'boldmessage': "Context Dict Message For Tracks", 'track_list': category_list}
    return render(request, 'trec/tracks.html', context_dict)


# View for personal user profile page
# Find User / Researcher and return info in dict.
def profile(request):
    username = request.user
    research = Researcher.objects.get(user=username)
    user = User.objects.get(username=username)

    context_dict = {'user': user, 'researcher': research}

    return render(request, 'trec/profile.html', context_dict)
    
    
    

def edit_profile(request):
    """Handles user profile editing by fetching form data and altering the database"""
    context_dict = {}

    username = request.user
    user = User.objects.get(username=username)
    research = Researcher.objects.get(user=user)


    # alter db
    if request.method == 'POST':
        # user_form = EditUserInfoForm(data=request.POST)

        profile_form = EditUserInfoForm(data=request.POST)

        if profile_form.is_valid():
            profile = profile_form.save(commit=False)
            research.display_name = profile.display_name
            research.save()
			
     #      user = profile_form.save(commit=False)
            # handle picture change
     #       if 'picture' in request.FILES:
      #          profile.picture = request.FILES['picture']

            # save changes
         #   user.save()
            profile.save()
            print "Profile saved"
        else:
          #  print user_form.errors
            print profile_form.errors
        
    else:
        # user_form = EditUserInfoForm(instance=request.user)
        profile_form = UserProfileForm(instance=request.user)

    # context_dict['user_form'] = user_form
    context_dict['profile_form'] = profile_form
    # context_dict['picture'] = request.user.userprofile.picture
    return render(request, "trec/profile.html", context_dict)
