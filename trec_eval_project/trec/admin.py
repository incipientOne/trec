from django.contrib import admin
from trec.models import Researcher, Track, Task, Run

class TaskAdmin(admin.ModelAdmin):
	list_display = ['title', 'track', 'task_url']

	def __unicode__(self):
		return self.title


class TrackAdmin(admin.ModelAdmin):
	prepopulated_fields = {'slug':('title', )}

admin.site.register(Researcher)
admin.site.register(Track, TrackAdmin)
admin.site.register(Task, TaskAdmin)
admin.site.register(Run)