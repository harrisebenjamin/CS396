from django.forms import ModelForm, Form, ChoiceField, RadioSelect
from django.forms.widgets import TextInput, Textarea, FileInput, URLInput, NumberInput

from .models import Lesson, Quiz, Question

class LessonForm(ModelForm):
    class Meta:
        model = Lesson
        fields = ["title", "content", "link", "file"]

        widgets = {
            'title' : TextInput(attrs= {'class' : 'form-control', 'placeholder' : 'Title'}),
            'content' : Textarea(attrs= {'class' : 'form-control', 'placeholder' : 'Content', 'rows' : '10'}),
            'file' : FileInput(attrs={'class' : 'form-control'}),
            'link' : URLInput(attrs= {'class' : 'form-control', 'placeholder' : 'Link'})
        }


class QuizForm(ModelForm):
    class Meta:
        model = Quiz
        fields = ["title", "numOfQuestions"]

        labels = {'numOfQuestions': 'Number of Questions'}

        widgets = {
            'title' : TextInput(attrs= {'class' : 'form-control', 'placeholder' : 'Title'}),
            'numOfQuestions' : NumberInput(attrs={'class': 'form-control', 'placeholder': '0'}),
        }


class QuestionForm(ModelForm):
    class Meta:
        model = Question
        fields = ['question', 'option1', 'option2', 'option3', 'option4', 'answer']

        labels = {'option1': 'Answer 1', 'option2': 'Answer 2', 'option3': 'Answer 3', 'option4': 'Answer 4'}

        widgets = {
            'question' : TextInput(attrs={'class': 'form-control', 'placeholder': 'Question'}),
            'option1' : TextInput(attrs={'class': 'form-control', 'placeholder': 'Answer 1'}),
            'option2' : TextInput(attrs={'class': 'form-control', 'placeholder': 'Answer 2'}),
            'option3' : TextInput(attrs={'class': 'form-control', 'placeholder': 'Answer 3'}),
            'option4' : TextInput(attrs={'class': 'form-control', 'placeholder': 'Answer 4'}),
        }  


class AnswerForm(Form):
    CHOICES = [
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4')
    ]

    answer = ChoiceField(
        widget=RadioSelect,
        choices=CHOICES
    )