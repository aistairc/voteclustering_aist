from django.test import TestCase
from AIST_survey.models import Choice
from .test_question_model import QuestionModelTests


class ChoiceModelTests(TestCase):
    def test_is_empty(self):
        saved_choices = Choice.objects.all()
        self.assertEquals(saved_choices.count(), 0)

    def test_creating_choice(self):
        self.create_choice()

        saved_choices = Choice.objects.all()
        self.assertEquals(saved_choices.count(), 1)

    def create_choice(self, text='Test'):
        choice = Choice()

        choice.question = QuestionModelTests().create_question()
        choice.text = text

        choice.save()

        return choice
