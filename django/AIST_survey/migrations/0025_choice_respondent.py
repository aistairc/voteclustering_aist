# Generated by Django 2.1.3 on 2020-08-12 09:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('AIST_survey', '0024_auto_20200318_1855'),
    ]

    operations = [
        migrations.AddField(
            model_name='choice',
            name='respondent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='AIST_survey.Respondent'),
        ),
    ]
