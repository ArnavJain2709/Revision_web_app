from django.contrib import admin
from .models import QuizSubject, QuestionPack, Question, UserPerformance
# Register your models here.
admin.site.register(QuizSubject)
admin.site.register(QuestionPack)
admin.site.register(Question)
admin.site.register(UserPerformance)
