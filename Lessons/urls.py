from django.urls import path
from . import views

urlpatterns = [
    path('', views.lessonsView, name='lessons'),
    path('createLesson', views.createLesson, name='createLesson'),
    path('viewLesson/<lessonID>', views.viewLesson, name='viewLesson'),
    path('createQuiz', views.createQuiz, name='createQuiz'),
    path('createQuiz/createQuestions/<quizID>', views.createQuestions, name='createQuestions'),
    path('quiz/<quizID>', views.takeQuiz, name='takeQuiz'),
    path('quiz/viewResults/<quizID>', views.quizResults, name='quizResults'),
]