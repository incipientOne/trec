from django.shortcuts import render
from django.http import HttpResponse

def about(request):
  context_dict = {'boldmessage': "Context Dict Message"}
  return render(request, 'trec/about.html', context_dict)


def home(request):
  context_dict = {'boldmessage': "Context Dict Message"}
  return render(request, 'trec/home.html', context_dict)