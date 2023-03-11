from django.urls import path
from . import views

app_name = 'teacher'

urlpatterns = [
    path('', views.index, name='index'),
    path('createQuestionPack/', views.createQuestionPack,
         name='createQuestionPack'),
    path('addQuestions/', views.addQuestions, name='addQuestions'),
    path('addFlashCard/', views.addFlashCard, name='addFlashCard'),
    path('userDashboard/', views.userDashboard, name='userDashboard'),
]
