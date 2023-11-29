from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from plotly.offline import plot
import plotly.graph_objects as go


from userposts.forms import PostForm
from userposts.models import UserPost
from .models import Group, Course, CourseGrade
from Lessons.models import Lesson, Quiz, StudentScore
from Lessons.forms import LessonForm, QuizForm
from .forms import SignupForm, teacherForm
from Lessons.views import Percentile

# Create your views here.

@login_required
def index(request):
    currentCourse = Course.objects.get(name = 'General')
    userPosts = UserPost.objects.all().filter(course = currentCourse).order_by('-createdOn')
    userGroup = Group.objects.get(user = request.user)
    if request.method == "POST":
        form  = PostForm(request.POST, request.FILES)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user
            obj.course = currentCourse
            obj.save()
            return HttpResponseRedirect(reverse('home'))
    else:
        form = PostForm()

    return render(request, 'index.html', {"form": form, "userPosts": userPosts, "userGroup": userGroup},)
    

@login_required
def profile(request):
    userPosts = UserPost.objects.all().filter(user = request.user).order_by('-createdOn')
    return render(request, 'profile.html', {"userPosts": userPosts})



def signup(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        form2 = teacherForm(request.POST)
        if form.is_valid():
            obj = form.save()
            obj2 = form2.save(commit=False)
            obj2.user = obj
            obj2.save()
            return HttpResponseRedirect(reverse('login'))
    else:
        form = SignupForm()
        form2 = teacherForm()

    return render(request, 'registration/signup.html', {"form": form, "form2": form2})


@login_required
def courses(request):
    courseList = Course.objects.all().exclude(name = 'General').order_by('name')
    return render(request, 'courses.html', {"courseList": courseList})


@login_required
def courseDiscussionBoard(request, courseID=None):
    course = Course.objects.get(id = courseID)
    userPosts = UserPost.objects.all().filter(course = course).order_by('-createdOn')
    userGroup = Group.objects.get(user = request.user)
    if request.method == "POST":
        form  = PostForm(request.POST, request.FILES)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user
            obj.course = course
            obj.save()
            return redirect('courseDiscussionBoard', course.id)
    else:
        form = PostForm()

    return render(request, 'courseDiscussionBoard.html', {'course': course, 'userPosts': userPosts, 'userGroup': userGroup, 'form': form})


@login_required
def courseLessons(request, courseID=None):
    userGroup = Group.objects.get(user = request.user)
    course = Course.objects.get(id = courseID)
    lessons = Lesson.objects.all().filter(course = course)

    return render(request, 'courseLessons.html', {'userGroup': userGroup, 'course': course, 'lessons': lessons})


@login_required
def courseQuizzes(request, courseID=None):
    userGroup = Group.objects.get(user = request.user)
    course = Course.objects.get(id = courseID)
    quizzes = Quiz.objects.all().filter(course = course)
    studentScores = StudentScore.objects.filter(student = request.user)
    scoreQuizzes = StudentScore.objects.filter(student = request.user).values_list('quiz', flat=True)

    percentiles = []
    for score in studentScores:
        percentiles.append(Percentile(targetScore=score.score, targetQuiz=score.quiz))
        

    return render(request, 'courseQuizzes.html', {'userGroup': userGroup, 'course': course, 'quizzes': quizzes, 'studentScores': studentScores, 'scoreQuizzes': scoreQuizzes, 'percentiles': percentiles})


@login_required
def courseGrades(request, courseID=None):
    userGroup = Group.objects.get(user = request.user)
    course = Course.objects.get(id = courseID)

    scores = StudentScore.objects.filter(course = courseID).order_by('quiz').order_by('score')
    quizzes = Quiz.objects.filter(course = course)

    grades = CourseGrade.objects.filter(course = course).order_by('-grade')
    gradeValues = calcGrades(grades=grades)

    figure = go.Figure(
        data=go.Pie(
            title='Course Grades',
            labels=['A', 'B', 'C', 'D', 'F'],
            values = list(gradeValues),
            sort=False
        )
    )
    graph = plot(figure, auto_open=False, output_type='div', show_link=False)

    return render(request, 'courseGrades.html', {'userGroup': userGroup, 'course': course, 'grades': grades, 'quizzes': quizzes, 'scores': scores, 'graph': graph})

@login_required
def courseGradesDesc(request, courseID=None):
    userGroup = Group.objects.get(user = request.user)
    course = Course.objects.get(id = courseID)

    scores = StudentScore.objects.filter(course = courseID).order_by('quiz').order_by('-score')
    quizzes = Quiz.objects.filter(course = course)

    grades = CourseGrade.objects.filter(course = course).order_by('grade')
    gradeValues = calcGrades(grades=grades)

    figure = go.Figure(
        data=go.Pie(
            title='Course Grades',
            labels=['A', 'B', 'C', 'D', 'F'],
            values = list(gradeValues),
            sort=False
        )
    )
    graph = plot(figure, auto_open=False, output_type='div', show_link=False)

    return render(request, 'courseGrades.html', {'userGroup': userGroup, 'course': course, 'grades': grades, 'quizzes': quizzes, 'scores': scores, 'graph': graph})

@login_required
def courseGradesAvg(request, courseID=None):
    userGroup = Group.objects.get(user = request.user)
    course = Course.objects.get(id = courseID)

    grades = StudentScore.objects.filter(course = courseID).order_by('quiz').order_by('-score')
    quizzes = Quiz.objects.filter(course = course)

    return render(request, 'courseGrades.html', {'userGroup': userGroup, 'course': course, 'grades': grades, 'quizzes': quizzes})


@login_required
def studentCourseGrade(request, courseID=None):
    userGroup = Group.objects.get(user = request.user)
    course = Course.objects.get(id = courseID)

    scores = StudentScore.objects.filter(course = courseID, student = request.user)
    grade = CourseGrade.objects.filter(course = course, student = request.user)

    return render(request, 'studentCourseGrade.html', {'userGroup': userGroup, 'course': course, 'grade': grade, 'scores': scores})




@login_required
def courseCreateLesson(request, courseID=None):
    course = Course.objects.get(id = courseID)
    if request.method == "POST":
        form = LessonForm(request.POST, request.FILES)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user
            obj.course = course
            obj.save()
            return redirect('lessons')
    else:
        form = LessonForm()

    return render(request, 'createLesson.html', {"form": form})


@login_required
def courseCreateQuiz(request, courseID=None):
    course = Course.objects.get(id = courseID)
    if request.method == "POST":
        form = QuizForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.course = course
            obj.save()
            return redirect('createQuestions', obj.id)
    else:
        form = QuizForm()

    return render(request, 'createQuiz.html', {"form": form}) 



def calcGrades(grades):
    values = [0, 0, 0, 0, 0]

    for grade in grades:
        if grade.grade == 'A':
            values[0] += 1
        elif grade.grade == 'B':
            values[1] += 1
        elif grade.grade == 'C':
            values[2] += 1
        elif grade.grade == 'D':
            values[3] += 1
        else:
            values[4] += 1

    return values
        