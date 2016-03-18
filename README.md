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

* Pull this repo
* Go to trec_eval_project/
* run `python manage.py migrate` to set up basic server data
* run `python manage.py bower install` to set up front-end dependencies
* run `python manage.py collectstatic` to copy and prepare front-end
* You can now run the server