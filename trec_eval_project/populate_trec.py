import os
from django.core.files import File
from django.contrib.auth.hashers import make_password
from trec_eval_project.settings import BASE_DIR

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'trec_eval_project.settings')

import django

django.setup()

from trec.models import Researcher, Track, Task, Run, Run_type, Query_type, Feedback_type
from django.contrib.auth.models import User


def populate():
    test_qrel = os.path.join(BASE_DIR, 'pop script data', 'qrels', 'aq.trec2005.qrels.txt')
    test_run = os.path.join(BASE_DIR, 'pop script data', 'runs', 'aq.trec.bm25.0.50.res.txt')

    # add superuser
    add_user('admin', '', 'adminpass', is_superuser=True)

    # requred example users.
    add_user('jill', '', 'jill')
    add_user('jim', '', 'jim')
    add_user('joe', '', 'jow')

    # turn some users into researchers
    jill = add_researcher('jill', 'jill', )

    # add tracks
    add_Track('test_track_1', 'http://www.google.com', 'Description - A simple track for tests.', 'Genre - tester')

    # add tasks
    add_Task('test_track_1', 'test_task_1', 'http://www.google.com', 'Description - A simple task...', 1990, test_qrel)
    add_Task('test_track_1', 'test_task_2', 'http://www.google.com', 'Description - Testing purpose only', 1990, test_qrel)

    # add runs
    add_run('jill',
            'test_task_1',
            'test_run_1',
            'a test run',
            test_run,
            Run_type.AUTOMATIC,
            Query_type.OTHER,
            Feedback_type.NONE)


def add_user(username, email, password, is_superuser=False):
    password = make_password(password) # get_or_create does not hash the password, so we do so here.
    defaults = {'email': email,
                'password': password,
                'is_staff': is_superuser,
                'is_superuser': is_superuser}
    u = User.objects.get_or_create(username=username, defaults=defaults)[0]
    u.save()
    return u


def add_researcher(username, display_name, website='', organisation='', picture=None):
    defaults = {'website': website,
                'organisation': organisation,
                'display_name': display_name,
                'profile_picture': picture}
    user = User.objects.filter(username=username)[0]
    r = Researcher.objects.get_or_create(user=user,
                                         defaults=defaults)[0]
    r.save()
    return r


def add_Track(title, url, description, genre):
    t = Track.objects.get_or_create(title=title,
                                    track_url=url,
                                    description=description,
                                    genre=genre)[0]
    t.save()
    return t


def add_Task(track_title, title, url, description, year, qrel_file_path):
    qrel_file = File(open(qrel_file_path))
    track = Track.objects.filter(title=track_title)[0]
    defaults = {'track': track,
                'task_url': url,
                'description': description,
                'year': year,
                'judgements_file': qrel_file}
    t = Task.objects.get_or_create(title=title, defaults=defaults)[0]
    t.save()
    return t


def add_run(researcher_name, task_title, name, description, results_file_path, run_type, query_type, feedback_type):
    results_file = File(open(results_file_path))
    user = User.objects.filter(username=researcher_name)[0]
    researcher = Researcher.objects.filter(user=user)[0]
    task = Task.objects.filter(title=task_title)[0]
    defaults = {'researcher': researcher,
                'task': task,
                'description': description,
                'result_file': results_file,
                'run_type': run_type,
                'query_type': query_type,
                'feedback_type': feedback_type}
    r = Run.objects.get_or_create(name=name, defaults=defaults)[0]
    r.save()
    return r


if __name__ == '__main__':
    populate()
