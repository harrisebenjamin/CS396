from django.db import models
from django.conf import settings

from Education.models import Course

User = settings.AUTH_USER_MODEL

# Create your models here.

class UserPost(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    content = models.TextField()
    createdOn = models.DateTimeField(auto_now_add=True)
    file1 = models.FileField(null=True, blank=True, upload_to="documents/")
    file2 = models.FileField(null=True, blank=True, upload_to="documents/")
    file3 = models.FileField(null=True, blank=True, upload_to="documents/")
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.title} ({self.user})'
    
    


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(UserPost, on_delete=models.CASCADE)
    content = models.TextField()
    createdOn = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.post} {self.pk}'