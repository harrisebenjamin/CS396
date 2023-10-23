from typing import Any
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Group
from django.forms.widgets import TextInput, PasswordInput, CheckboxInput


class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "username", "password1", "password2"]
        widgets = {
            'first_name' : TextInput(attrs= {'class' : 'form-control', 'placeholder' : 'First Name'}),
            'last_name' : TextInput(attrs= {'class' : 'form-control', 'placeholder' : 'Last Name'}),
            'username' : TextInput(attrs= {'class' : 'form-control', 'placeholder' : 'Username'})
        }

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)

        self.fields['password1'].widget = PasswordInput(attrs= {'class' : 'form-control', 'placeholder' : 'Password'})
        self.fields['password2'].widget = PasswordInput(attrs= {'class' : 'form-control', 'placeholder' : 'Confirm Password'})


class teacherForm(ModelForm):
    class Meta:
        model = Group
        fields = ["isTeacher"]
        labels = {"isTeacher": "Are you a teacher?"}
        widgets = {
            'isTeacher' : CheckboxInput(attrs= {'class' : 'form-check-input'})
        }