from django.urls import path

from . import views
app_name = 'flashcard'


urlpatterns = [
    path('', views.index, name='index'),
    path('flashcardPackDisplay/', views.flashcardPackDisplay,
         name='flashcardPackDisplay'),
    path('flashcardDisplay/', views.flashcardDisplay,
         name='flashcardDisplay'),
]
