from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL

# Create your models here.

class UserPost(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    content = models.TextField()
    createdOn = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title