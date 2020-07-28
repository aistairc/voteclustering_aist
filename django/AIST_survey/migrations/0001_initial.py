# Generated by Django 2.1.3 on 2019-01-07 08:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Choice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Enquete',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('term_url', models.URLField()),
                ('published_at', models.DateTimeField()),
                ('expired_at', models.DateTimeField(blank=True, null=True)),
                ('finished_at', models.DateTimeField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Like',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('choice', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='AIST_survey.Choice')),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=20)),
                ('text', models.TextField()),
                ('enquete', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='questions', to='AIST_survey.Enquete')),
            ],
        ),
        migrations.CreateModel(
            name='Respondent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('attribute', models.CharField(max_length=255)),
                ('enquete', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='AIST_survey.Enquete')),
            ],
        ),
        migrations.CreateModel(
            name='SuggestedChoice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('choice', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='AIST_survey.Choice')),
                ('respondent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='AIST_survey.Respondent')),
            ],
        ),
        migrations.AddField(
            model_name='like',
            name='respondent',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='AIST_survey.Respondent'),
        ),
        migrations.AddField(
            model_name='choice',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='choices', to='AIST_survey.Question'),
        ),
    ]