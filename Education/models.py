from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Group(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    isTeacher = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user} {self.isTeacher}'
    

class Course(models.Model):
    name = models.CharField(max_length=75)
    teacher = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.name
    

class CourseGrade(models.Model):
    CHOICES = [
        ('A', 'A'),
        ('B', 'B'),
        ('C', 'C'),
        ('D', 'D'),
        ('F', 'F'),
    ]

    student = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    grade = models.CharField(max_length=1, choices=CHOICES, default='A')

    def __str__(self):
        return f'{self.student} {self.course} {self.grade}'
    