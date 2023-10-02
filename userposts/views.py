from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http import HttpResponseRedirect

from .models import UserPost

# Create your views here.
@login_required
def deletePost(request, postID=None):
    targetPost = UserPost.objects.get(id = postID)
    targetPost.delete()
    return HttpResponseRedirect(reverse('home'))