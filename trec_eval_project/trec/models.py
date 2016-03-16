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


# Models used
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
# Combination of run name and a unique number, e.g. run_name-1
# Used to slug the url
    run_id = models.TextField(unique=True)

    run_type = models.IntegerField(default=Run_type.AUTOMATIC)
    
    query_type = models.IntegerField(default=Query_type.TITLE)
    
    feedback_type = models.IntegerField(default=Feedback_type.NONE)
# Values used in the graphs / tables - Table values = MAP, P10, P20
    map_val = models.FloatField(null=True, blank=True)
    
    p5 = models.FloatField(null=True, blank=True)
    p10 = models.FloatField(null=True, blank=True)
    p15 = models.FloatField(null=True, blank=True)
    p20 = models.FloatField(null=True, blank=True)
    p30 = models.FloatField(null=True, blank=True)
    p100 = models.FloatField(null=True, blank=True)
    p200 = models.FloatField(null=True, blank=True)
    p500 = models.FloatField(null=True, blank=True)
    p1000 = models.FloatField(null=True, blank=True)
    
    recall00 = models.FloatField(null=True, blank=True)
    recall01 = models.FloatField(null=True, blank=True)
    recall02 = models.FloatField(null=True, blank=True)
    recall03 = models.FloatField(null=True, blank=True)
    recall04 = models.FloatField(null=True, blank=True)
    recall05 = models.FloatField(null=True, blank=True)
    recall06 = models.FloatField(null=True, blank=True)
    recall07 = models.FloatField(null=True, blank=True)
    recall08 = models.FloatField(null=True, blank=True)
    recall09 = models.FloatField(null=True, blank=True)
    recall10 = models.FloatField(null=True, blank=True)
    
    slug = models.SlugField()

    def save(self, *args, **kwargs):
        
        self.slug = slugify(self.run_id)
        
        # make sure that the result file is saved.
        super(Run, self).save(*args, **kwargs)

        # file paths for the qrel and results files.
        qrel_path = os.path.join(MEDIA_ROOT, self.task.judgements_file.url)
        results_path = os.path.join(MEDIA_ROOT, self.result_file.url)

        # calculate map, p_10, p_20.
        self.map_val, self.recall00, self.recall01, self.recall02, self.recall03, self.recall04, self.recall05, self.recall06, self.recall07, self.recall08, self.recall09, self.recall10, self.p5, self.p10, self.p15, self.p20, self.p30, self.p100, self.p200, self.p500, self.p1000 = tuple(trec_wrapper(qrel_path, results_path))

        super(Run, self).save()

    def __unicode__(self):
        return self.name
