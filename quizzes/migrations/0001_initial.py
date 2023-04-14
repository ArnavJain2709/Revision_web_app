# Generated by Django 3.2.17 on 2023-02-13 13:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='QuestionPack',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pack_name', models.CharField(max_length=100)),
                ('pack_description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='QuizSubject',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject_name', models.CharField(max_length=100)),
                ('subject_description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='UserPerformance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('questions_answered', models.PositiveIntegerField()),
                ('questions_correct', models.PositiveIntegerField()),
                ('pack', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quizzes.questionpack')),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quizzes.quizsubject')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='questionpack',
            name='subject',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quizzes.quizsubject'),
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question_text', models.TextField()),
                ('option_1', models.CharField(max_length=100)),
                ('option_2', models.CharField(max_length=100)),
                ('option_3', models.CharField(max_length=100)),
                ('option_4', models.CharField(max_length=100)),
                ('correct_option', models.PositiveSmallIntegerField()),
                ('pack', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quizzes.questionpack')),
            ],
        ),
    ]
