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
    
    slug = models.SlugField()
    
    # Slum Mckenzie up these URLS
    def save(self, *args, **kwargs):
        self.slug = slugify(self.user.username)
        super(Researcher, self).save(*args, **kwargs)
    
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
    p10_val = models.FloatField(null=True, blank=True)
    p20_val = models.FloatField(null=True, blank=True)

    slug = models.SlugField()

    def save(self, *args, **kwargs):

        self.slug = slugify(self.run_id)

        # make sure that the result file is saved.
        super(Run, self).save(*args, **kwargs)

        self.populate_with_trec_eval_data(self)

        super(Run, self).save()

    def __unicode__(self):
        return self.name

    def populate_with_trec_eval_data(self, run):
        if run.map_val == None:
            # file paths for the qrel and results files.
            qrel_path = os.path.join(MEDIA_ROOT, self.task.judgements_file.url)
            results_path = os.path.join(MEDIA_ROOT, self.result_file.url)

            # calculate map, p_10, p_20.
            map, rMap, pMap = trec_wrapper(qrel_path, results_path)
            run.map_val = map
            run.p10_val = pMap.get(10)
            run.p20_val = pMap.get(20)
            for key in rMap:
                r = Recall_val.objects.create(run=self, score=rMap[key], recall_number=key)
                r.save()

            for key in pMap:
                p = P_value.objects.create(run=self, score=pMap[key], p_number=key)
                p.save()

class P_value(models.Model):
    run = models.ForeignKey(Run)
    score = models.FloatField()
    p_number = models.IntegerField()  # ie is it p5, p10, etc?


class Recall_val(models.Model):
    run = models.ForeignKey(Run)
    score = models.FloatField()
    recall_number = models.FloatField()
