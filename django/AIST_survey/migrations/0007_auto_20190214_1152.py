# Generated by Django 2.1.3 on 2019-02-14 02:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AIST_survey', '0006_auto_20190131_0450'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='type',
            field=models.CharField(max_length=40),
        ),
    ]