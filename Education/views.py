from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from userposts.forms import PostForm
from userposts.models import UserPost
from django.urls import reverse

# Create your views here.

@login_required
def index(request):
    userPosts = UserPost.objects.all().order_by('-createdOn')
    if request.method == "POST":
        form  = PostForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user
            obj.save()
            return HttpResponseRedirect(reverse('home'))
    else:
        form = PostForm()

    return render(request, 'index.html', {"form": form, "userPosts": userPosts},)
    

@login_required
def profile(request):
    return render(request, 'profile.html')
        