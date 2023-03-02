from django.shortcuts import render
from django.http import HttpResponse
# for getting the logged-in user's data
from django.contrib.auth.models import User
# importing the models from the quizzes app
from quizzes.models import *
from django.shortcuts import redirect, render
from django.contrib import messages

# Create your views here.


def index(request):
    if request.user.is_authenticated:  # checks if the the current user is logged in
        username = request.user.username
        subjects = QuizSubject.objects.all()  # using the models from the quizzes app
        context = {
            'username': username,
            'subjects': subjects
        }
        return render(request, "flashcard/index.html", context)


def flashcardPackDisplay(request):
    if request.user.is_authenticated:

        if request.method == "POST":
            # Determining the flashcard subject chosen by the user
            subjectName = request.POST.get("subject")
            # for debugging purposes
            print("The selected subject is: ", subjectName)
            # Doing something with the subject value

            # Retrieving the matching subject record from the QuizSubjects model
            quiz_subject = QuizSubject.objects.get(subject_name=subjectName)
            # Filtering the QuestionPack table for records with the corresponding QuizSubject
            question_packs = QuestionPack.objects.filter(subject=quiz_subject)
            # passing the list of question packs as context so that they can be shown on the test.html page
            return render(request, "quizzes/subjectQuizzes.html", {"question_packs": question_packs})
        else:
            # Render the template without any information
            return render(request, "quizzes/test.html")

    else:
        messages.error(
            request, "You do not have permission to view this page!")
        # "return redirect('home')" redirects the user to the home route defined in the urls.py file of the main app called Revision_web_app
        return redirect('home')
