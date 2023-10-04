from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Group(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    isTeacher = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user} {self.isTeacher}'