from django import forms
from django.contrib.auth.models import User
from trec.models import Track, Task, Researcher, Run

class UserForm(forms.ModelForm):
	password = forms.CharField(widget=forms.PasswordInput())
	
	class Meta:
		model = User
		fields = ('username', 'email', 'password')
		
class UserProfileForm(forms.ModelForm):
	class Meta:
		model = Researcher
		fields = ('display_name', 'website', 'organisation','profile_picture')

