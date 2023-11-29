from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name = 'home'),
    path('profile', views.profile, name = 'profile'),
    path('accounts/signup', views.signup, name = 'signup'),
    path('courses', views.courses, name='courses'),
    path('course/discussionBoard/<courseID>', views.courseDiscussionBoard, name='courseDiscussionBoard'),
    path('course/lessons/<courseID>', views.courseLessons, name='courseLessons'),
    path('course/quizzes/<courseID>', views.courseQuizzes, name='courseQuizzes'),
    path('course/grades/<courseID>', views.courseGrades, name='courseGrades'),
    path('course/grades/d/<courseID>', views.courseGradesDesc, name='courseGradesDesc'),
    path('course/studentGrades/<courseID>', views.studentCourseGrade, name='studentCourseGrades'),
    path('course/createLesson/<courseID>', views.courseCreateLesson, name='courseCreateLesson'),
    path('course/createQuiz/<courseID>', views.courseCreateQuiz, name='courseCreateQuiz'),
]