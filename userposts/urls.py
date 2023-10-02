from django.urls import path
from . import views

urlpatterns = [
    path('delete/<postID>', views.deletePost, name='delete'),
    path('view/<postID>', views.viewPost, name='view'),
    path('update/<postID>', views.updatePost, name='update'),
    path('comment/delete/<commentID>', views.deleteComment, name='deleteComment'),
]