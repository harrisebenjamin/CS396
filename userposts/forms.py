from django.forms import ModelForm
from .models import UserPost, Comment

class PostForm(ModelForm):
    class Meta:
        model = UserPost
        fields = ["title", "content"]


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ["content"]