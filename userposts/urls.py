from django.urls import path
from . import views

urlpatterns = [
    path('delete/<postID>', views.deletePost, name='delete'),
]