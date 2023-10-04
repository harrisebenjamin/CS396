from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse


from userposts.forms import PostForm
from userposts.models import UserPost
from .models import Group
from .forms import SignupForm, teacherForm

# Create your views here.

@login_required
def index(request):
    userPosts = UserPost.objects.all().order_by('-createdOn')
    userGroup = Group.objects.get(user = request.user)
    if request.method == "POST":
        form  = PostForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user
            obj.save()
            return HttpResponseRedirect(reverse('home'))
    else:
        form = PostForm()

    return render(request, 'index.html', {"form": form, "userPosts": userPosts, "userGroup": userGroup},)
    

@login_required
def profile(request):
    userPosts = UserPost.objects.all().filter(user = request.user).order_by('-createdOn')
    return render(request, 'profile.html', {"userPosts": userPosts})



def signup(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        form2 = teacherForm(request.POST)
        if form.is_valid():
            obj = form.save()
            obj2 = form2.save(commit=False)
            obj2.user = obj
            obj2.save()
            return HttpResponseRedirect(reverse('login'))
    else:
        form = SignupForm()
        form2 = teacherForm()

    return render(request, 'registration/signup.html', {"form": form, "form2": form2})
        