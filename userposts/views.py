from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import redirect

from .models import UserPost, Comment
from .forms import CommentForm
from Education.models import Group

# Create your views here.
@login_required
def deletePost(request, postID=None):
    targetPost = UserPost.objects.get(id = postID)
    targetPost.delete()
    return HttpResponseRedirect(reverse('home'))


@login_required
def viewPost(request, postID=None):
    post = UserPost.objects.get(id = postID)
    comments = Comment.objects.all().filter(post = postID).order_by("-createdOn")
    userGroup = Group.objects.get(user = request.user)

    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid:
            obj = form.save(commit=False)
            obj.user = request.user
            obj.post = post
            obj.save()
            # return HttpResponseRedirect(reverse('home'))
            return redirect('view', postID)
    else:
        form = CommentForm()

    return render(request, 'viewPost.html', {"form": form, "post": post, "comments": comments, "userGroup": userGroup})


@login_required
def updatePost(request, postID=None):
    post = UserPost.objects.get(id = postID)
    return render(request, 'updatePost.html', {"post": post})


@login_required
def deleteComment(request, commentID=None):
    targetComment  = Comment.objects.get(id = commentID)
    postID = targetComment.post.id
    targetComment.delete()
    return redirect('view', postID)