from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.contrib import messages

# Create your views here.


def index(request):

    if request.user.is_authenticated:
        username = request.user.username
        fname = request.user.username

        return render(request, "quizzes/index.html", {'fname': fname})
    else:
        messages.error(request, "Please Login / Register!")
        return redirect('home')
