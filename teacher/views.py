from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth.models import User
# importing the models from the quizzes app
from quizzes.models import *

# Create your views here.


def index(request):
    if request.user.is_superuser:
        test_message = "You are an admin and this page is working!"
        return render(request, 'teacher/index.html', {'test_message': test_message})
    else:
        messages.error(
            request, "You do not have permission to view this page!")
        return redirect('home')


def createQuestionPack(request):
    if request.user.is_superuser:
        teacher = request.user.username
        subjects = QuizSubject.objects.all()  # get all subjects from database
        context = {
            'teacher': teacher,
            'subjects': subjects
        }
        # code for handling the form data that
        # will be used to create a new QuestionPack model object
        # so that a new Question Pack can be created
        if request.method == 'POST':
            pack_name = request.POST.get('pack_name')
            pack_description = request.POST.get('pack_description')
            subject_id = request.POST.get('subject')
            subject = QuizSubject.objects.get(pk=subject_id)

            # creating a new QuestionPack model object:
            new_pack = QuestionPack(
                pack_name=pack_name, pack_description=pack_description, subject=subject)
            new_pack.save()  # saving the new object to QuestionPack model
            messages.success(
                request, "New question pack called {pack_name} has just been created.")
            return render(request, 'teacher/index.html')
        else:
            return render(request, 'teacher/newPack.html', context)
        return render(request, 'teacher/newPack.html', context)
    else:
        messages.error(
            request, "You do not have permission to view this page!")
        return redirect('home')


def addQuestions(request):
    if request.user.is_superuser:
        teacher = request.user.username
        packs = QuestionPack.objects.all()  # get all subjects from database
        context = {
            'teacher': teacher,
            'packs': packs
        }
        # code for handling the form data that
        # will be used to create a new Question model object
        # so that a new Question can be created
        if request.method == 'POST':
            question_text = request.POST.get('question_text')
            pack_id = request.POST.get('pack')
            option_1 = request.POST.get('option_1')
            option_2 = request.POST.get('option_2')
            option_3 = request.POST.get('option_3')
            option_4 = request.POST.get('option_4')
            correct_option = request.POST.get('correct_option')
            pack = QuestionPack.objects.get(pk=pack_id)

            pack_name = pack.pack_name

            # creating a new QuestionPack model object:
            new_question = Question(
                question_text=question_text,
                pack=pack,
                option_1=option_1,
                option_2=option_2,
                option_3=option_3,
                option_4=option_4,
                correct_option=correct_option)

            new_question.save()  # saving the new object to Question model
            messages.success(
                request, "New question has just been added to the pack called", pack_name, "has just been created.")
            return render(request, 'teacher/index.html')
        else:
            return render(request, 'teacher/newQuestions.html', context)
        return render(request, 'teacher/newQuestions.html', context)
    else:
        messages.error(
            request, "You do not have permission to view this page!")
        return redirect('home')


def userDashboard(request):
    if not request.user.is_superuser:
        messages.error(
            request, "You do not have permission to view this page!")
        return redirect('home')

    users = User.objects.all()
    performance_data = {}
    for user in users:
        performances = user.userperformance_set.all()
        performance_data[user.username] = [{'date': str(
            perf.date), 'score': perf.score_percentage, 'subject': str(perf.subject)} for perf in performances]
        context = {
            'users': users,
            'performance_data': performance_data
        }

    return render(request, 'teacher/userDashboard.html', context)