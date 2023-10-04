from django.forms import ModelForm
from .models import UserPost, Comment

class PostForm(ModelForm):
    class Meta:
        model = UserPost
        fields = ["title", "content", "file1", "file2", "file3"]


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ["content"]