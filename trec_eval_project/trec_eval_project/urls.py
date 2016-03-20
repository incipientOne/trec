"""trec_eval_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings

from registration.backends.simple.views import RegistrationView

"""
class MyRegistrationView(RegistrationView):
    def get_success_url(self, user, request):
        return '/trec/'
"""

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^trec/', include('trec.urls')),
    #url(r'^accounts/register/$', MyRegistrationView.as_view(), name='registration_register'),
    url(r'^accounts/', include('registration.backends.simple.urls')),
    )
    
# UNDERNEATH your urlpatterns definition, add the following two lines:

if settings.DEBUG:
    urlpatterns += patterns('django.views.static', (r'^media/(?P<path>.*)', 'serve',
                            {'document_root': settings.MEDIA_ROOT}), )
