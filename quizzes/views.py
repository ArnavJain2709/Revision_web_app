from django.shortcuts import render
from django.http import HttpResponse
# for getting the logged-in user's data
from django.contrib.auth.models import User
# importing the models required for quizzes
from .models import *
from django.shortcuts import redirect, render
from django.contrib import messages

# Create your views here.


def index(request):

    if request.user.is_authenticated:  # checks if the the current user is logged in
        username = request.user.username

        return render(request, "quizzes/index.html", {'username': username})
    else:
        messages.error(request, "Please Login / Register!")
        return redirect('home')


# creating a view function for displaying questions packs
def questionPackDisplay(request):

    if request.method == "POST":
        # Determining the quiz subject chosen by the user
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


def quizGame(request):
    if request.method == "POST":
        questionPackName = request.POST.get("packName")
        question_pack = QuestionPack.objects.get(pack_name=questionPackName)
        print('Pack selected: ', question_pack)

        # getting the questions:
        questions = question_pack.question_set.all()

        # questions = Question.objects.filter(pack=questionPackName)
        return render(request, 'quizzes/quiz.html', {'questions': questions, 'question_pack_id': question_pack.id})
    else:

        return render(request, "quizzes/test.html")


def submit_quiz(request, pack_id):
    score = 0
    question_count = Question.objects.filter(pack_id=pack_id).count()
    # loop that iterates through each key-value pair in the POST data from the quiz.html form
    for key, value in request.POST.items():
        # checks if the key starts with "question"
        if key.startswith('question'):
            # Gets the primary key of the Question object from the key
            question_id = key.replace('question', '')
            # Get the corresoinding Question object from the database
            question = Question.objects.get(pk=question_id)
            # Checks if the selected answer matches the correct_option in the "question" model
            if int(value) == question.correct_option:
                score += 1
    score_percentage = (score / question_count) * 100
    score_percentage = round(score_percentage, 1)
    return render(request, 'quizzes/quiz_results.html', {'score_percentage': score_percentage})
