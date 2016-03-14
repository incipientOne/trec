from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from trec_eval.trec_wrapper import trec_wrapper
from trec_eval_project.settings import MEDIA_ROOT
import os.path

# Enumerated types for Run:
from enum import Enum

# Needed to slug URLS 
from django.template.defaultfilters import slugify

class Run_type(Enum):	
    AUTOMATIC = 1
    MANUAL = 2


class Query_type(Enum):
    TITLE = 1
    TITLE_AND_DESCRIPTION = 2
    DESCRIPTION = 3
    ALL = 4
    OTHER = 5


class Feedback_type(Enum):
    NONE = 1
    PSEUDO = 2
    RELEVANCE = 3
    OTHER = 4


# Models
class Researcher(models.Model):
    user = models.OneToOneField(User, primary_key=True)

    profile_picture = models.ImageField(upload_to='profile_images', blank=True)
    website = models.URLField(blank=True)
    display_name = models.CharField(max_length=128)
    organisation = models.CharField(max_length=128)

    def __unicode__(self):
        return self.user.username


class Track(models.Model):
    title = models.CharField(max_length=128, unique=True)
    track_url = models.URLField()
    description = models.TextField()
    genre = models.CharField(max_length=128)
    
    slug = models.SlugField()
    
    # Slum Mckenzie up these URLS
    def save(self, *args, **kwargs):
    	self.slug = slugify(self.title)
    	super(Track, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.title


class Task(models.Model):
    track = models.ForeignKey(Track)
    title = models.CharField(max_length=128, unique=True)
    task_url = models.URLField()
    description = models.TextField()
    year = models.IntegerField()
    judgements_file = models.FileField(upload_to='qrels')
    
    slug = models.SlugField()
    
    # Slum Mckenzie up these URLS
    def save(self, *args, **kwargs):
    	self.slug = slugify(self.title)
    	super(Task, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.title


class Run(models.Model):
    researcher = models.ForeignKey(Researcher)
    task = models.ForeignKey(Task)
    name = models.CharField(max_length=128)
    description = models.TextField()
    result_file = models.FileField(upload_to='runs')

    run_type = models.IntegerField(default=Run_type.AUTOMATIC)
    
    query_type = models.IntegerField(default=Query_type.TITLE)
    
    feedback_type = models.IntegerField(default=Feedback_type.NONE)

    map = models.FloatField(null=True, blank=True)
    p10 = models.FloatField(null=True, blank=True)
    p20 = models.FloatField(null=True, blank=True)

    def save(self, *args, **kwargs):
        # make sure that the result file is saved.
        super(Run, self).save(*args, **kwargs)

        # file paths for the qrel and results files.
        qrel_path = os.path.join(MEDIA_ROOT, self.task.judgements_file.url)
        results_path = os.path.join(MEDIA_ROOT, self.result_file.url)

        # calculate map, p_10, p_20.
        self.map, self.p10, self.p20 = trec_wrapper(qrel_path, results_path)

        super(Run, self).save()

    def __unicode__(self):
        return self.name
