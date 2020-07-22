import json
import logging
from datetime import datetime, timezone

from django.conf import settings
from django.core import serializers
from django.shortcuts import get_object_or_404
from django.views import generic
from django.core.serializers.json import DjangoJSONEncoder

from AIST_survey.models.choice import Choice
from AIST_survey.models.enquete import Enquete
from AIST_survey.models.evaluation import Evaluation
from AIST_survey.models.question import Question
from AIST_survey.models.respondent import Respondent


class LiteIndexView(generic.TemplateView):
    template_name = "AIST_survey/lite_index.html"
    is_outside_public_period = False
    template_message = ""

    def get(self, request, **kwargs):
        # 公開期間外の場合はテンプレートを公開期間外であることを示すためのものに差し替え
        enquete = get_object_or_404(Enquete, unique_url=self.kwargs['unique_url'])
        if enquete.published_at > datetime.now(timezone.utc):
            self.is_outside_public_period = True
            self.template_name = "AIST_survey/outside_public_period.html"
            self.template_message = "現在このアンケートは公開開始前です。"
        elif enquete.expired_at is not None:
            if enquete.expired_at < datetime.now(timezone.utc):
                self.is_outside_public_period = True
                self.template_name = "AIST_survey/outside_public_period.html"
                self.template_message = "このアンケートの回答期間は既に終了しています。"
        return super().get(request, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # 公開期間外の場合はメッセージのみをcontextに格納
        if self.is_outside_public_period:
            context["template_message"] = self.template_message
            return context

        enquete = get_object_or_404(Enquete, unique_url=self.kwargs['unique_url'])

        context['enquete'] = enquete
        questions = Question.objects.filter(enquete_id=enquete.pk)
        data = serializers.serialize("model_to_dict", questions)

        logger = logging.getLogger('development')

        for question_item in data:
            if question_item["type"] != "question":
                choices = Choice.objects.filter(question_id=question_item["id"])
                if choices:
                    choices_dict = serializers.serialize("model_to_dict", choices)
                    if question_item["with_answered_num"]:
                        for choice in choices_dict:
                            choice["answered_num"] = Evaluation.objects.filter(choice_id=choice["id"],
                                                                               like__gte=1).count()
                    question_item["choices"] = choices_dict

        # cls=DjangoJSONEncoderを追加した
        json_data = json.dumps(data, cls=DjangoJSONEncoder)
        logger.debug("Question_JSON : \n" + json_data)
        context['questions'] = json_data

        context['respondent_attribute_max_length'] = Respondent._meta.get_field("attribute").max_length
        context['choice_text_max_length'] = Choice._meta.get_field("text").max_length

        # フロントエンド側にDEBUGであるかどうかの値を送信
        context['is_debug'] = settings.DEBUG

        return context


