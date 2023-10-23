from django.forms import ModelForm
from .models import UserPost, Comment
from django.forms.widgets import TextInput, Textarea, FileInput

class PostForm(ModelForm):
    class Meta:
        model = UserPost
        fields = ["title", "content", "file1",]# "file2", "file3"]
        widgets = {
            'title' : TextInput(attrs= {'class' : 'form-control', 'placeholder' : 'Title'}),
            'content' : Textarea(attrs= {'class' : 'form-control', 'placeholder' : 'Content', 'rows' : '3'}),
            'file1' : FileInput(attrs={'class' : 'form-control'}),
            # 'file2' : FileInput(attrs={'class' : 'form-control'}),
            # 'file3' : FileInput(attrs={'class' : 'form-control'})
        }


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ["content"]
        widgets = {
            'content' : Textarea(attrs= {'class' : 'form-control', 'placeholder' : 'Comment', 'rows' : '2'})
        }