from django.db import models
from django.utils.translation import gettext_lazy

from . import Enquete


class Question(models.Model):
    @staticmethod
    def create_question_type(description, has_other_select, has_post_respondent, has_placeholder):
        return {"description": description,
                "has_other_select": has_other_select,
                "has_post_respondent": has_post_respondent,
                "has_placeholder": has_placeholder}

    def __str__(self):
        return self.text

    USERID = 'userid'
    QUESTION = 'question'
    SINGLE = 'single'
    MULTI = 'multi'

    TYPE_CHOICES = [
        (USERID, 'userid'),
        (QUESTION, 'question'),
        (SINGLE, 'single'),
        (MULTI, 'multi'),
    ]

    enquete = models.ForeignKey(Enquete, on_delete=models.CASCADE, related_name='questions')
    type = models.CharField(max_length=40, choices=TYPE_CHOICES)
    text = models.TextField()
    is_skip_allowed = models.BooleanField(default=True)
    min_like_required = models.IntegerField(default=0)
    example_answer = models.TextField(blank=True, null=True)
    with_answered_num = models.BooleanField(default=False)
    without_select = models.BooleanField(default=False)
    is_result_public = models.BooleanField(default=True)

    type_dict = {
        USERID: create_question_type.__func__(description=gettext_lazy('回答者のID（学籍番号など）の入力欄'),
                                              has_other_select=False,
                                              has_post_respondent=False,
                                              has_placeholder=True),
        QUESTION: create_question_type.__func__(description=gettext_lazy('自由記述形式の質問'),
                                                has_other_select=True,
                                                has_post_respondent=True,
                                                has_placeholder=True),
        SINGLE: create_question_type.__func__(description=gettext_lazy('単一選択の質問(ボタン型)'),
                                              has_other_select=False,
                                              has_post_respondent=True,
                                              has_placeholder=False),
        MULTI: create_question_type.__func__(description=gettext_lazy('複数選択の質問(ボタン型)'),
                                             has_other_select=False,
                                             has_post_respondent=True,
                                             has_placeholder=False),
    }
