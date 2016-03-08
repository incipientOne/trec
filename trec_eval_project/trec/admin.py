from django.contrib import admin
from trec.models import Researcher, Track, Task, Run

admin.site.register(Researcher)
admin.site.register(Track)
admin.site.register(Task)
admin.site.register(Run)