from django.test import TestCase
from AIST_survey.models import Question
from .test_enquete_model import EnqueteModelTests


class QuestionModelTests(TestCase):
    def test_is_empty(self):
        saved_questions = Question.objects.all()
        self.assertEquals(saved_questions.count(), 0)

    def test_creating_question(self):
        self.create_question()

        saved_questions = Question.objects.all()
        self.assertEquals(saved_questions.count(), 1)

    def create_question(self, type='Test', text='Test', is_skip_allowed=False, min_like_required=2,
                        example_answer='Test', with_answered_num=True, without_select=True):
        question = Question()

        question.enquete = EnqueteModelTests().create_enquete()
        question.type = type
        question.text = text
        question.is_skip_allowed = is_skip_allowed
        question.min_like_required = min_like_required
        question.example_answer = example_answer
        question.with_answered_num = with_answered_num
        question.without_select = without_select

        question.save()

        return question
