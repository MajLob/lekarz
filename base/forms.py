from django.forms import ModelForm
from .models import Room
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
import django_filters
 


class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = '__all__'
        exclude = ['host', 'participants']
        

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2' ]