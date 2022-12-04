from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from .forms import NewPost, RegisterUser
from .models import Post
from django.contrib.auth.decorators import login_required


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
    if request.method == 'GET':
        blogpost = Post.objects.all()
        return render(request, 'blog.html', {
            'blogpost': blogpost
            })
    else:
        print(request.POST)
        return render(request, 'home.html')


@login_required
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


@login_required
def update_post(request, post_id):
    if request.method == 'GET':
        post = get_object_or_404(Post, pk=post_id, user=request.user)
        form = NewPost(instance=post)
        return render(request, 'post_detail.html', {'form': form, 'post': post})
    else:
        try:
            post = get_object_or_404(Post, pk=post_id, user=request.user)
            form = NewPost(request.POST, instance=post)
            form.save()
            return redirect('blog')
        except ValueError:
            return render(request, 'post_detail.html', {'form': form, 'post': post, 'error': 'Error editing post'})


@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id, user=request.user)
    if request.method == 'POST':
        post.delete()
        return redirect('blog')


@login_required
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


@login_required
def user_profile(request):
    posts = Post.objects.filter(user=request.user)
    return render(request, 'profile.html', {'posts': posts})


