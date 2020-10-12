# Generated by Django 3.0.5 on 2020-05-08 19:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0016_remove_question_degradation'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='quiz',
            name='ended',
        ),
        migrations.RemoveField(
            model_name='quiz',
            name='started',
        ),
        migrations.CreateModel(
            name='QuizState',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('started', models.BooleanField(default=False)),
                ('ended', models.BooleanField(default=False)),
                ('question', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='quiz.Question')),
                ('quiz', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quiz.Quiz')),
                ('round', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='quiz.Round')),
            ],
        ),
        migrations.CreateModel(
            name='QuizRoom',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quiz', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quiz.Quiz')),
            ],
        ),
    ]