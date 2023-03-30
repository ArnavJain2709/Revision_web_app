from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth.models import User
from django.urls import reverse
# importing the models from the quizzes app
from quizzes.models import *
# importing the form
from .forms import QuestionForm

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
        # else:
            form = QuestionForm()
            return render(request, 'teacher/index.html', {'form': form})
        # else:
     #   return redirect('home')
        return render(request, 'teacher/newPack.html', context)
    else:
        messages.error(
            request, "You do not have permission to view this page!")
        return redirect('home')

# Creating 2 view functions to delete question packs:
# the first function will just display all of the records in
# QuestionPack model in the form of a table:


def questionPackList(request):
    question_packs = QuestionPack.objects.all()
    context = {'question_packs': question_packs}
    return render(request, 'teacher/questionPackList.html', context)

# Creating the 2nd view function that deletes the selected question packs:


def deleteQuestionPacks(request):
    if request.method == 'POST':
        question_pack_ids = request.POST.getlist('question_packs')
        QuestionPack.objects.filter(id__in=question_pack_ids).delete()
    return redirect('teacher:questionPackList')


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
                request, "New question has just been has just been created.")
            return redirect('teacher:index')
        else:
            return render(request, 'teacher/newQuestions.html', context)
        return render(request, 'teacher/newQuestions.html', context)
    else:
        messages.error(
            request, "You do not have permission to view this page!")
        return redirect('home')


def deleteQuestionsPackDisplay(request):
    if request.user.is_superuser:
        teacher = request.user.username
        packs = QuestionPack.objects.all()  # get all subjects from database
        context = {
            'teacher': teacher,
            'packs': packs
        }
        return render(request, 'teacher/deleteQuestionsPackDisplay.html', context)
    else:
        messages.error(
            request, "You do not have permission to view this page!")
        return redirect('home')


def deleteQuestionsList(request):
    # print('Hello World!')
    if request.user.is_authenticated:

        if request.method == "POST":
            # Determining the flashcard pack chosen by the user
            pack = request.POST.get("packName")
            question_pack = QuestionPack.objects.get(
                pack_name=pack)
            questions = Question.objects.filter(pack=question_pack)

            # for debugging purposes
            # print("The selected subject is: ", question_pack)

            # code for rendering the flashcards on the
            context = {
                'questions': questions,
            }
            return render(request, "teacher/deleteQuestions.html", context)
        else:
            return redirect('home')

    else:
        messages.error(
            request, "You need to login!")
        # "return redirect('home')" redirects the user to the home route defined in the urls.py file of the main app called Revision_web_app
        return redirect('home')


def deleteQuestionExecution(request):
    if request.method == 'POST':
        question_ids = request.POST.getlist('question')
        Question.objects.filter(id__in=question_ids).delete()
        teacher = request.user.username
        packs = QuestionPack.objects.all()  # get all subjects from database
        context = {
            'teacher': teacher,
            'packs': packs
        }
        return redirect('teacher:deleteQuestionsPackDisplay')
    else:
        messages.error(
            request, "Problem with POST request!")
        # "return redirect('home')" redirects the user to the home route defined in the urls.py file of the main app called Revision_web_app
        return redirect('home')


def addFlashCard(request):
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
            prompts = request.POST.get('prompts')
            pack_id = request.POST.get('pack')
            content = request.POST.get('content')
            question_pack = QuestionPack.objects.get(pk=pack_id)
            subject = question_pack.subject

            # pack_name = question_pack.pack_name

            # creating a new QuestionPack model object:
            new_flashcard = Card(
                prompts=prompts,
                question_pack=question_pack,
                content=content,
                subject=subject)
            new_flashcard.save()  # saving the new object to Question model
            messages.success(
                request, "New flashcard has just been has just been created.")
            return render(request, 'teacher/index.html')
        else:
            return render(request, 'teacher/newFlashCard.html', context)
        return render(request, 'teacher/newFlashcard.html', context)
    else:
        messages.error(
            request, "You do not have permission to view this page!")
        return redirect('home')


def deleteFlashcardPackDisplay(request):
    if request.user.is_superuser:
        teacher = request.user.username
        packs = QuestionPack.objects.all()  # get all subjects from database
        context = {
            'teacher': teacher,
            'packs': packs
        }
        return render(request, 'teacher/deleteFlashcardPackDisplay.html', context)
    else:
        messages.error(
            request, "You do not have permission to view this page!")
        return redirect('home')


def deleteFlashcardList(request):
    if request.user.is_authenticated:

        if request.method == "POST":
            # Determining the flashcard pack chosen by the user
            pack = request.POST.get("packName")
            flashcardPack = QuestionPack.objects.get(
                pack_name=pack)
            flashcards = Card.objects.filter(question_pack=flashcardPack)

            # for debugging purposes
            # print("The selected subject is: ", question_pack)

            # code for rendering the flashcards on the
            context = {
                'flashcards': flashcards,
            }
            return render(request, "teacher/deleteFlashcard.html", context)

    else:
        messages.error(
            request, "You need to login!")
        # "return redirect('home')" redirects the user to the home route defined in the urls.py file of the main app called Revision_web_app
        return redirect('home')


def deleteFlashcardExecution(request):
    if request.method == 'POST':
        flashcard_ids = request.POST.getlist('flashcard')
        Card.objects.filter(id__in=flashcard_ids).delete()
        teacher = request.user.username
        packs = Card.objects.all()  # get all subjects from database
        context = {
            'teacher': teacher,
            'packs': packs
        }
        return redirect('teacher:deleteFlashcardPackDisplay')
    else:
        messages.error(
            request, "Problem with POST request!")
        # "return redirect('home')" redirects the user to the home route defined in the urls.py file of the main app called Revision_web_app
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
