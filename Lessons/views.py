from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import redirect

from .models import Lesson
from .forms import LessonForm
from Education.models import Group

# Create your views here.
@login_required
def lessonsView(request):
    lessons = Lesson.objects.all().order_by('-createdOn')
    userGroup = Group.objects.get(user = request.user)
    return render(request, 'lessons.html', {"lessons": lessons, "userGroup": userGroup})


@login_required
def createLesson(request):
    if request.method == "POST":
        form = LessonForm(request.POST, request.FILES)
        if form.is_valid:
            obj = form.save(commit=False)
            obj.user = request.user
            obj.save()
            return redirect('lessons')
    else:
        form = LessonForm()

    return render(request, 'createLesson.html', {"form": form})


@login_required
def viewLesson(request, lessonID=None):
    lesson = Lesson.objects.get(id = lessonID)
    return render(request, 'viewLesson.html', {"lesson": lesson})