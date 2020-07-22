from django.test import TestCase
from AIST_survey.models import Respondent
from .test_enquete_model import EnqueteModelTests


class RespondentModelTests(TestCase):
    def test_is_empty(self):
        saved_respondents = Respondent.objects.all()
        self.assertEquals(saved_respondents.count(), 0)

    def test_creating_respondent(self):
        self.create_respondent()

        saved_respondents = Respondent.objects.all()
        self.assertEquals(saved_respondents.count(), 1)

    def create_respondent(self, attribute='Test'):
        respondent = Respondent()

        respondent.enquete = EnqueteModelTests().create_enquete()
        respondent.attribute = attribute

        respondent.save()

        return respondent
