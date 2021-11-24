from django import forms
from django.db.models import fields
from django.contrib.auth.forms import UserCreationForm
from . models import *


class NotesForm(forms.ModelForm):
    class Meta:
        model = Notes
        fields = ['title', 'description']


class DashboardForm(forms.Form):
    text = forms.CharField(max_length=255, label='Search News')


class ToDoForm(forms.ModelForm):
    class Meta:
        model = ToDo
        fields = ['title', 'completed']


class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']
