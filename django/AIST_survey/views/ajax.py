import json
import logging

from django.core import serializers
from django.http import JsonResponse
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Q

from AIST_survey.models.choice import Choice
from AIST_survey.models.enquete import Enquete
from AIST_survey.models.evaluation import Evaluation
from AIST_survey.util.add_answer import add_answer, get_client_ip


# パスワード認証を行う関数
def ajax_check_password(request):
    input_password = request.POST.get('password')
    enquete_id = request.POST.get('enquete_id')

    d = {
        # check_password()では入力したパスワードと対象となるEnqueteクラスのインスタンスを引数として比較を行う
        'result': Enquete.check_password(Enquete.objects.get(pk=enquete_id), input_password)
    }

    return JsonResponse(d)


# 他者の意見を取得する関数
def ajax_get_others_opinion(request):
    logger = logging.getLogger('development')
    choices = Choice.objects.random(question_id=int(request.POST.get('question_id')),
                                    size=int(request.POST.get('choice_size')))

    choices_dict = serializers.serialize("model_to_dict", choices)

    for choices_content in choices_dict:
        choices_content['num'] = \
            Evaluation.objects.filter(Q(choice_id=choices_content['id']), Q(assessment=Evaluation.LIKED) |
                                      Q(assessment=Evaluation.PROPOSED)).count()
        choices_content['key'] = choices_content.pop('id')

    logger.debug("Choice_JSON : \n" + json.dumps(choices_dict, cls=DjangoJSONEncoder))

    d = {
        # check_password()では入力したパスワードと対象となるEnqueteクラスのインスタンスを引数として比較を行う
        'opinion_list': choices_dict
    }

    return JsonResponse(d)


def get_assessment(is_selected):
    if is_selected:
        return Evaluation.LIKED
    else:
        return Evaluation.PRESENTED


# アンケート結果を受信し、データベースに追加を行う関数
def ajax_add_answer(request):
    logger = logging.getLogger('development')
    answer_list_json = request.POST.get('answer_list')
    answer_list = json.loads(answer_list_json)
    respondent_data_json = request.POST.get('respondent_data')
    respondent_data = json.loads(respondent_data_json)
    logger.debug("answer_list: \n" + json.dumps(answer_list))
    ip = get_client_ip(request)
    add_answer(request.POST.get('enquete_id'), answer_list, respondent_data, ip)

    d = {}
    return JsonResponse(d)


# 入力フォームの内容を受け取り、サジェストの一覧を返す関数
def ajax_suggest(request):
    question_id = request.POST.get('question_id')
    input_value = request.POST.get('input_value')
    loaded_keys = json.loads(request.POST.get('loaded_keys'))

    suggested_choices = Choice.objects.filter(
        question_id=question_id, text__icontains=input_value).exclude(pk__in=loaded_keys)
    choices_dict = serializers.serialize("model_to_dict", suggested_choices)

    for choices_content in choices_dict:
        choices_content['num'] = Evaluation.objects.filter(choice_id=choices_content['id'], like__gte=1).count()
        choices_content['key'] = choices_content.pop('id')

    d = {
        'suggested_choice': choices_dict
    }
    return JsonResponse(d)
