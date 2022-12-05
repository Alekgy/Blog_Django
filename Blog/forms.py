from .models import Post
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class RegisterUser(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name =  forms.CharField(required=True)
    last_name = forms.CharField(required=True)

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

class NewPost(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'text']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Write a title of post'}),
            'text': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Write a text of post'}),
        }

