from django.forms import ModelForm
from .models import Post
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class RegisterUser(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name =  forms.CharField()
    last_name = forms.CharField()

    class meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'email',
            'username',
            'password1',
            'password2'
        ]

class NewPost(ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'text']

