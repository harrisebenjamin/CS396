from django.urls import path
from . import views

urlpatterns = [
    path('', views.lessonsView, name='lessons'),
    path('createLesson', views.createLesson, name='createLesson'),
    path('viewLesson/<lessonID>', views.viewLesson, name='viewLesson'),
]