from django.urls import path

from . import views
app_name = 'quizzes'

urlpatterns = [
    path('', views.index, name='index'),
    path('questionPackDisplay/', views.questionPackDisplay,
         name='questionPackDisplay'),
    path('quizGame/', views.quizGame,
         name='quizGame'),
    path('<int:pack_id>/submit/', views.submit_quiz, name='submit_quiz'),
    # path('submit_quiz/', views.submit_quiz, name='submit_quiz'),
]
