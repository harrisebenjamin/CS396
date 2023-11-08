from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name = 'home'),
    path('profile', views.profile, name = 'profile'),
    path('accounts/signup', views.signup, name = 'signup'),
    path('courses', views.courses, name='courses'),
]