# Generated by Django 2.1.3 on 2019-07-31 16:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AIST_survey', '0015_evaluation_assessment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='evaluation',
            name='assessment',
            field=models.CharField(choices=[('liked', 'liked'), ('presented', 'presented'), ('proposed', 'proposed'), ('disliked', 'disliked')], max_length=40),
        ),
    ]
