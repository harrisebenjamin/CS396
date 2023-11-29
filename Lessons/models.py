from django.db import models
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator

from Education.models import Course

user = settings.AUTH_USER_MODEL

# Create your models here.
class Lesson(models.Model):
    user = models.ForeignKey(user, on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    content = models.TextField()
    createdOn = models.DateTimeField(auto_now_add=True)
    link = models.URLField(null=True, blank=True)
    file = models.FileField(null=True, blank=True, upload_to='documents/')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, default=Course.objects.get(name = 'General').id)

    def __str__(self):
        return f'{self.title} {self.createdOn}'


class Quiz(models.Model):
    title = models.CharField(max_length=50)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    numOfQuestions = models.IntegerField()

    def __str__(self):
        return self.title
    

class Question(models.Model):

    CHOICES = [
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
    ]

    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    questionNumber = models.IntegerField(default=1)
    question = models.TextField()
    option1 = models.CharField(max_length=250, default='')
    option2 = models.CharField(max_length=250, default='')
    option3 = models.CharField(max_length=250, default='')
    option4 = models.CharField(max_length=250, default='')
    answer = models.CharField(max_length=1, choices=CHOICES, default='1')

    def __str__(self):
        return f'{self.quiz} {self.question}'
    

class StudentScore(models.Model):
    student = models.ForeignKey(user, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    score = models.FloatField()
    attemptNumber = models.IntegerField(default=2)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, default=Course.objects.get(name = 'General').id)

    def __str__(self):
        return f'{self.student} {self.quiz} {self.score}'