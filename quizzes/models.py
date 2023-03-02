from django.db import models
from django.contrib.auth.models import User
# for timezpne.now() in the UserPerformance model:
from django.utils import timezone

# Create your models here.


class QuizSubject(models.Model):
    subject_name = models.CharField(max_length=100)
    subject_description = models.TextField()

    def __str__(self):
        return self.subject_name


class QuestionPack(models.Model):
    pack_name = models.CharField(max_length=100)
    pack_description = models.TextField()
    subject = models.ForeignKey(QuizSubject, on_delete=models.CASCADE)

    def __str__(self):
        return self.pack_name


class Question(models.Model):
    question_text = models.TextField()
    pack = models.ForeignKey(QuestionPack, on_delete=models.CASCADE)
    option_1 = models.CharField(max_length=100)
    option_2 = models.CharField(max_length=100)
    option_3 = models.CharField(max_length=100)
    option_4 = models.CharField(max_length=100)
    correct_option = models.PositiveSmallIntegerField()

    def __str__(self):
        return self.question_text


class UserPerformance(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.ForeignKey(QuizSubject, on_delete=models.CASCADE)
    pack = models.ForeignKey(QuestionPack, on_delete=models.CASCADE)
    score_percentage = models.FloatField(
        default=0.0)  # sets the default value to 0
    date = models.DateTimeField(default=timezone.now)

    # def __str__(self):
    #    return self.user
    def __str__(self):
        return f"{self.user.username} - {self.pack.pack_name} - {self.score_percentage}"
