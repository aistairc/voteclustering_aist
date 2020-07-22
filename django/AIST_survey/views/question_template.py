from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView

from AIST_survey.models.enquete import Enquete


class QuestionTemplateView(TemplateView):
    template_name = "AIST_survey/question.html"

    def get_context_data(self, **kwargs):
        enquete = get_object_or_404(Enquete, unique_url=self.kwargs['unique_url'])
        context = super().get_context_data(**kwargs)
        # 利用規約の改行コードを<br>に置換
        context['term_of_service'] = enquete.term_of_service.splitlines()
        # map(lambda line: "<li>" + line + "</li>", enquete.term_of_service.splitlines())
        # context['term_of_service'] = ''.join(map(lambda line: "<li>" + line + "</li>", enquete.term_of_service.splitlines()))
        return context
