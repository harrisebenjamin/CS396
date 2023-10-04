from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Group


class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "username", "password1", "password2"]

class teacherForm(ModelForm):
    class Meta:
        model = Group
        fields = ["isTeacher"]
        labels = {"isTeacher": "Are you a teacher?"}