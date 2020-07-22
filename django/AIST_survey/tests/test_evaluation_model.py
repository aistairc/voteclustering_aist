from django.test import TestCase
from AIST_survey.models import Evaluation
from .test_choice_model import ChoiceModelTests
from .test_respondent_model import RespondentModelTests


class EvaluationModelTests(TestCase):
    def test_is_empty(self):
        saved_evaluations = Evaluation.objects.all()
        self.assertEquals(saved_evaluations.count(), 0)

    def test_creating_evaluation(self):
        self.create_evaluation()

        saved_evaluations = Evaluation.objects.all()
        self.assertEquals(saved_evaluations.count(), 1)

    def create_evaluation(self, like=1):
        evaluation = Evaluation()

        evaluation.respondent = RespondentModelTests().create_respondent()
        evaluation.choice = ChoiceModelTests().create_choice()
        evaluation.like = like

        evaluation.save()

        return evaluation
