# Generated by Django 2.1.3 on 2019-07-31 07:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AIST_survey', '0014_respondent_timestamp'),
    ]

    operations = [
        migrations.AddField(
            model_name='evaluation',
            name='assessment',
            field=models.CharField(choices=[('like', 'like'), ('presented', 'presented'), ('dislike', 'dislike')], default='like', max_length=40),
            preserve_default=False,
        ),
    ]
