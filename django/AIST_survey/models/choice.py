import random

from django.db import models
from . import Question
# なぜか . からRespondentがimportできなかった
from .respondent import Respondent
from django.utils import timezone


class ChoiceManager(models.Manager):
    # 指定された数の選択肢をランダム抽出し、リストを返す
    def random(self, question_id, size):
        choices = self.filter(question_id=question_id)

        if choices.count() >= size:
            random_int_list = random.sample(range(choices.count()), size)
        else:
            random_int_list = random.sample(range(choices.count()), choices.count())

        random_query = []
        for i in random_int_list:
            random_query.append(choices[i])

        return random_query


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='choices')
    respondent = models.ForeignKey(Respondent, blank=True, null=True, on_delete=models.CASCADE)
    text = models.TextField(max_length=500)
    objects = ChoiceManager()
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.text
