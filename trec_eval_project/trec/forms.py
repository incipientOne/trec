from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from trec.models import Track, Task, Researcher, Run


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = Researcher
        fields = ('display_name', 'website', 'organisation')


# to edit user info
class EditUserInfoForm(forms.ModelForm):
    class Meta:
        model = Researcher
        fields = ('display_name', 'website', 'organisation', 'profile_picture')


# to edit user info
class AddRun(forms.ModelForm):
    class Meta:
        model = Run

        fields = ('name', 'description', 'result_file')

    def clean(self):
        if (self.cleaned_data.get('result_file') == None):
            raise ValidationError("Must upload a run file.")