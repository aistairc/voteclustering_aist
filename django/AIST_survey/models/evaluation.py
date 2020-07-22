from django.db import models
from . import Respondent, Choice
from django.utils import timezone


class Evaluation(models.Model):
    LIKED = 'liked'
    PRESENTED = 'presented'
    PROPOSED = 'proposed'
    DISLIKED = 'disliked'
    ASSESSMENT_CHOICES = [
        (LIKED, 'liked'),
        (PRESENTED, 'presented'),
        (PROPOSED, 'proposed'),
        (DISLIKED, 'disliked'),
    ]

    respondent = models.ForeignKey(Respondent, on_delete=models.CASCADE)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)
    like = models.IntegerField()
    assessment = models.CharField(max_length=40, choices=ASSESSMENT_CHOICES)
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return str(self.like)
