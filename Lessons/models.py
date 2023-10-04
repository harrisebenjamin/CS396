from django.db import models
from django.conf import settings

user = settings.AUTH_USER_MODEL

# Create your models here.
class Lesson(models.Model):
    user = models.ForeignKey(user, on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    content = models.TextField()
    createdOn = models.DateTimeField(auto_now_add=True)
    link = models.URLField(null=True, blank=True)
    file = models.FileField(null=True, blank=True, upload_to='documents/')

    def __str__(self):
        return f'{self.title} {self.createdOn}'