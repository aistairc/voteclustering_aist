# Generated by Django 2.1.3 on 2019-04-19 07:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('AIST_survey', '0010_enquete_unique_url'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='enquete',
            name='term_url',
        ),
    ]