# Generated by Django 2.1.3 on 2019-04-19 09:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AIST_survey', '0011_remove_enquete_term_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='choice',
            name='text',
            field=models.TextField(max_length=500),
        ),
    ]
