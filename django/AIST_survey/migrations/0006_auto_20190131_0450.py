# Generated by Django 2.1.3 on 2019-01-31 04:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('AIST_survey', '0005_question_example_answer'),
    ]

    operations = [
        migrations.RenameField(
            model_name='question',
            old_name='is_allowed_skip',
            new_name='is_skip_allowed',
        ),
    ]
