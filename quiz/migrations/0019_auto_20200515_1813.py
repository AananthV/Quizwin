# Generated by Django 3.0.5 on 2020-05-15 12:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0018_quizparticipant'),
    ]

    operations = [
        migrations.CreateModel(
            name='Audio',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('audio', models.URLField()),
            ],
        ),
        migrations.AlterField(
            model_name='questionscores',
            name='score',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='slide',
            name='type',
            field=models.CharField(choices=[('T', 'Text'), ('I', 'Image'), ('A', 'Audio')], max_length=1),
        ),
    ]