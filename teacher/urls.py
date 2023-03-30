from django.urls import path
from . import views

app_name = 'teacher'

urlpatterns = [
    path('', views.index, name='index'),
    path('createQuestionPack/', views.createQuestionPack,
         name='createQuestionPack'),
    path('addQuestions/', views.addQuestions, name='addQuestions'),
    path('deleteQuestionsPackDisplay/', views.deleteQuestionsPackDisplay,
         name='deleteQuestionsPackDisplay'),
    path('deleteQuestionsList/', views.deleteQuestionsList,
         name='deleteQuestionsList'),
    path('deleteQuestionExecution/', views.deleteQuestionExecution,
         name='deleteQuestionExecution'),
    path('addFlashCard/', views.addFlashCard, name='addFlashCard'),
    path('deleteFlashcardPackDisplay/', views.deleteFlashcardPackDisplay,
         name='deleteFlashcardPackDisplay'),
    path('deleteFlashcardList/', views.deleteFlashcardList,
         name='deleteFlashcardList'),
    path('deleteFlashcardExecution/', views.deleteFlashcardExecution,
         name='deleteFlashcardExecution'),
    path('questionPackList/', views.questionPackList, name='questionPackList'),
    path('deleteQuestionPacks/', views.deleteQuestionPacks,
         name='deleteQuestionPacks'),
    path('userDashboard/', views.userDashboard, name='userDashboard'),
]
