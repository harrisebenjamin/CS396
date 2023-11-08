from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import redirect

from .models import Lesson, Quiz, Question
from .forms import LessonForm, QuizForm, QuestionForm, AnswerForm
from Education.models import Group, Course

currentCourse = Course.objects.get(name = 'General')

# Create your views here.
@login_required
def lessonsView(request):
    lessons = Lesson.objects.all().filter(course = currentCourse).order_by('-createdOn')
    quizzes = Quiz.objects.all().filter(course = currentCourse)
    userGroup = Group.objects.get(user = request.user)
    return render(request, 'lessons.html', {"lessons": lessons, "quizzes": quizzes, "userGroup": userGroup})


@login_required
def createLesson(request):
    if request.method == "POST":
        form = LessonForm(request.POST, request.FILES)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user
            obj.save()
            return redirect('lessons')
    else:
        form = LessonForm()

    return render(request, 'createLesson.html', {"form": form})


@login_required
def viewLesson(request, lessonID=None):
    lesson = Lesson.objects.get(id = lessonID)
    return render(request, 'viewLesson.html', {"lesson": lesson})


@login_required
def createQuiz(request):
    if request.method == "POST":
        form = QuizForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.course = Course.objects.get(name = 'General')
            obj.save()
            #request.method = "GET"
            #return createQuestions(request=request, quiz=obj)
            return redirect('createQuestions', obj.id)
    else:
        form = QuizForm()

    return render(request, 'createQuiz.html', {"form": form}) 


@login_required
def createQuestions(request, quizID=None):
    quiz = Quiz.objects.get(id = quizID)
    forms = []
    if request.method == "POST":
        for i in range(quiz.numOfQuestions):
            forms.append(QuestionForm(request.POST, prefix=f'form{i}'))
        i = 1
        for form in forms:
            if form.is_valid():
                obj = form.save(commit=False)
                obj.quiz = quiz
                obj.questionNumber = i
                obj.save()
                i += 1
        return redirect('lessons')
    else:
        for i in range(quiz.numOfQuestions):
            forms.append(QuestionForm(prefix=f'form{i}'))

    return render(request, 'createQuestions.html', {'n' : range(quiz.numOfQuestions), 'forms' : forms})



@login_required
def takeQuiz(request, quizID=None):
    quiz = Quiz.objects.get(id = quizID)
    questions = Question.objects.all().filter(quiz = quizID).order_by("questionNumber")
    forms = []
    answers = []
    if request.method == "POST":
        for i in range(quiz.numOfQuestions):
            forms.append(AnswerForm(request.POST, prefix=f'form{i}'))
            forms[i].fields['answer'].choices = [(1, questions[i].option1), (2, questions[i].option2), (3, questions[i].option3), (4, questions[i].option4)]
        i = 1
        for form in forms:
            if form.is_valid():
                answers.append(form.cleaned_data.get('answer'))

        print(answers)
        return redirect('lessons')
    else:
        for i in range(quiz.numOfQuestions):
            forms.append(AnswerForm(prefix=f'form{i}'))
            forms[i].fields['answer'].choices = [(1, questions[i].option1), (2, questions[i].option2), (3, questions[i].option3), (4, questions[i].option4)]

    zipped = zip(questions, forms)
    return render(request, 'takeQuiz.html', {'quiz': quiz, 'zipped': zipped})