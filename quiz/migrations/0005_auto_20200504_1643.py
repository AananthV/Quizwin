# Generated by Django 3.0.5 on 2020-05-04 11:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0004_auto_20200504_1634'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Picture',
            new_name='Image',
        ),
        migrations.RenameField(
            model_name='image',
            old_name='picture',
            new_name='image',
        ),
    ]
