from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from .forms import NewPost, RegisterUser
from .models import Post


# Create your views here.


def home(request):
    return render(request, 'home.html')


def signup(request):
    if request.method == 'GET':
        return render(request, 'signup.html',
                      {"form": RegisterUser
                       })

    else:
        if request.POST["password1"] == request.POST["password2"]:
            try:
                user = User.objects.create_user(
                    username=request.POST['username'],
                    password=request.POST['password1'],
                    email=request.POST['email'],
                    first_name=request.POST['first_name'],
                    last_name=request.POST['last_name']
                )
                user.save()
                login(request, user)
                return redirect('blog')
            except IntegrityError:
                return render(request, 'signup.html', {
                    "form": RegisterUser,
                    'error': 'username already exist'
                })

        return render(request, 'signup.html', {
            "form": RegisterUser,
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
            new_post = form.save(commit=False)
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


def profile(request, user_username):
    posts = Post.objects.filter(user=user_username)
    return render(request, 'profile.html', {'posts': posts})


def user_profile(request):
    posts = Post.objects.filter(user=request.user)
    return render(request, 'profile.html', {'posts': posts})
