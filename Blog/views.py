from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from .forms import NewPost
from .models import Post

# Create your views here.


def home(request):
    return render(request, 'home.html')


def signup(request):
    if request.method == 'GET':
        return render(request, 'signup.html',
                      {"form": UserCreationForm
                       })

    else:
        if request.POST["password1"] == request.POST["password2"]:
            try:
                user = User.objects.create_user(
                    username=request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('blog')
            except IntegrityError:
                return render(request, 'signup.html', {
                    "form": UserCreationForm,
                    'error': 'username already exist'
                })

        return render(request, 'signup.html', {
            "form": UserCreationForm,
            'error': 'password do not match'
        })


def blog(request):
    blogpost = Post.objects.all()
    return render(request, 'blog.html', {
        'blogpost': blogpost
    })

def create_post(request):
    if request.method == 'GET':
        return render(request, 'create.html', {
            'form': NewPost
        })
    else:
        try:
            form = NewPost(request.POST)
            new_post= form.save(commit=False)
            new_post.user = request.user
            new_post.save()
            return redirect('blog')
        except ValueError:
             return render(request, 'create.html', {
            'form': NewPost,
            'error': 'please provide valid data'
            })


def signout(request):
    logout(request)
    return redirect('home')

def signin(request):
    if request.method == 'GET':
        return render(request, 'signin.html', {
            'form': AuthenticationForm
        })
    
    else:
        user = authenticate(
            request, 
            username=request.POST['username'], 
            password=request.POST['password'])
        
        if user is None:
            return render(request, 'signin.html', {
            'form': AuthenticationForm,
            'error': 'User or Password is incorrect'
        })
        else:
            login(request, user)
            return redirect('blog')
