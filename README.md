# Trec eval app #

This application is used to manage trec eval data. Follow the guidelines below to setup the project.

### What can users do? ###

* Non-logged user
    * Can view different tracks/runs/users
    * Can compare, filter, and sort different items in tables

* Logged user (researcher)
    * Can do the same things as non-logged user
    * Can crate his own profile and upload runs to different tasks
    * The results are marked for the user as to distinguish them in tables

* Admin
    * Can declare new tasks and upload qrel files for trec comparison.

### Setting up ###

Firstly make sure you are working on a clean pip environment.

`git pull` or `git clone` repo

`pip install -r requirements.txt --upgrade` in the root of pulled repo

`cd trec_eval_project/`

install a compiled copy of the trec_eval program in the trec_eval directory, named 'trec_eval'.

`python manage.py migrate`

`python manage.py bower install`

`python manage.py collectstatic`

Now you can run server/do stuff.