from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.db.models import Q

from .models import Lesson, Quiz, Question, StudentScore
from .forms import LessonForm, QuizForm, QuestionForm, AnswerForm
from Education.models import Group, Course

currentCourse = Course.objects.get(name = 'General')

# Create your views here.
@login_required
def lessonsView(request):
    lessons = Lesson.objects.all().filter(course = currentCourse).order_by('-createdOn')
    quizzes = Quiz.objects.all().filter(course = currentCourse)
    userGroup = Group.objects.get(user = request.user)
    studentScores = StudentScore.objects.filter(student = request.user)
    scoreQuizzes = StudentScore.objects.filter(student = request.user).values_list('quiz', flat=True)

    percentiles = []
    for score in studentScores:
        percentiles.append(Percentile(targetScore=score.score, targetQuiz=score.quiz))

    return render(request, 'lessons.html', {"lessons": lessons, "quizzes": quizzes, "userGroup": userGroup, 'studentScores': studentScores, 'scoreQuizzes': scoreQuizzes, 'percentiles': percentiles})


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
        for form in forms:
            if form.is_valid():
                answers.append(form.cleaned_data.get('answer'))
        numCorrect = 0
        for i in range(quiz.numOfQuestions):
            if answers[i] == questions[i].answer:
                numCorrect += 1
        score = (numCorrect / quiz.numOfQuestions) * 100

        if StudentScore.objects.filter(Q(student = request.user) & Q(quiz = quiz)).exists():
            obj = StudentScore.objects.get(Q(student = request.user) & Q(quiz = quiz))
            obj.score = score
            obj.attemptNumber -= 1
            obj.save()
        else:
            obj = StudentScore.objects.create(student=request.user, quiz=quiz, score=score, course=quiz.course)
            obj.save()
        return redirect('lessons')
    else:
        for i in range(quiz.numOfQuestions):
            forms.append(AnswerForm(prefix=f'form{i}'))
            forms[i].fields['answer'].choices = [(1, questions[i].option1), (2, questions[i].option2), (3, questions[i].option3), (4, questions[i].option4)]

    zipped = zip(questions, forms)
    return render(request, 'takeQuiz.html', {'quiz': quiz, 'zipped': zipped})


@login_required
def quizResults(request, quizID=None):
    quiz = Quiz.objects.get(id = quizID)
    quizScores = StudentScore.objects.all().filter(quiz = quiz)
    print(quizScores)
    return render(request, 'quizResults.html', {'quiz': quiz, "quizScores": quizScores})



class Percentile():
    def __init__(self, targetScore, targetQuiz):
        scores = StudentScore.objects.filter(quiz = targetQuiz)

        total = 0

        for score in scores:
            if score.score < targetScore:
                total += 1
        
        self.percentile = (total / scores.count()) * 100
        self.quiz = targetQuiz

