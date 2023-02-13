from django.shortcuts import render
from django.http import HttpResponse
# for getting the logged-in user's data
from django.contrib.auth.models import User
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


# creating a view function for computer science quizzes
def computerScience(request):
    fname = request.user.first_name
    return HttpResponse(request, "Hello {}", {'fname': fname})
