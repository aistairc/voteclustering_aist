from django.http import HttpResponse
from django.shortcuts import redirect
from django.views import generic
from django.db.models import Q
from django.utils import timezone
from django.core.serializers.json import DjangoJSONEncoder

from AIST_survey.models.enquete import Enquete
from AIST_survey.models.respondent import Respondent
from AIST_survey.models.evaluation import Evaluation
from AIST_survey.models.choice import Choice
from AIST_survey.models.question import Question

import json
import pandas as pd


def send_csv_from_json(json_to_csv):
    # pandasでcsv出力
    df = pd.read_json(json_to_csv).T

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=answerdata.csv'
    df.to_csv(path_or_buf=response, sep=',', float_format='%.2f', index=False, decimal=",")

    return response


def store_question_data(data_to_csv, question_texts, respondent_id, true_id):
    # 場合分けしてデータ格納
    for question_text in question_texts:
        if question_texts[question_text] == 'single' or question_texts[question_text] == 'multi':
            data_to_csv[respondent_id][question_text] = []
            q_evaluations = Evaluation.objects.filter(
                Q(respondent_id=true_id) & Q(choice__question__text=question_text))
            
            for evaluation in q_evaluations:
                data_to_csv[respondent_id][question_text].append(evaluation.choice.text)

        elif question_texts[question_text] == 'question':
            data_to_csv[respondent_id][question_text] = []
            q_evaluations = Evaluation.objects.filter(
                Q(respondent_id=true_id) & Q(choice__question__text=question_text) & Q(assessment='proposed'))
            
            # 文字数制限はいったん無くす
            # character_count = 5

            for evaluation in q_evaluations:
                # 文字数制限版
                # data_to_csv[respondent_id][question_text].append(evaluation.choice.text[0:character_count])

                data_to_csv[respondent_id][question_text].append(evaluation.choice.text)


def store_ip_data(data_to_csv, respondents, respondent_id, ip_dict, id_number):
    hashed_ip = respondents[respondent_id - 1].hashedIpAddress
    if hashed_ip not in ip_dict:
        ip_dict[hashed_ip] = {}
        ip_dict[hashed_ip]['id'] = id_number[0]
        id_number[0] += 1
        ip_dict[hashed_ip]['times'] = 1
    else:
        ip_dict[hashed_ip]['times'] += 1

    data_to_csv[respondent_id]['IP address'] = ip_dict[hashed_ip]['id']
    data_to_csv[respondent_id]['Number of responses'] = ip_dict[hashed_ip]['times']

    pass


def make_data_to_csv(respondents, questions):
    respondents_num = respondents.count()

    # csvのための{1:{},2:{},・・・}のような辞書を作る
    data_to_csv = {}
    for respondent_id in range(1, respondents_num + 1):
        data_to_csv[respondent_id] = {}

    # IPアドレス管理のための辞書データ
    ip_dict = {}
    # [0]しか使わない
    id_number = [1]

    # 質問リストを作る。（キー：質問文、バリュー：形式）
    question_texts = {}
    for qestion_part in questions:
        question_texts[qestion_part.text] = qestion_part.type

    for respondent_id in data_to_csv:
        data_to_csv[respondent_id]['ID'] = respondents[respondent_id - 1].id
        data_to_csv[respondent_id]['Attribute'] = respondents[respondent_id - 1].attribute
        store_ip_data(data_to_csv, respondents, respondent_id, ip_dict, id_number)
        data_to_csv[respondent_id]['Starting time'] = respondents[respondent_id - 1].startTime

        # 回答開始時間だけない場合のための条件分岐
        if respondents[respondent_id - 1].startTime is None:
            data_to_csv[respondent_id]['Duration'] = -1
        else:
            data_to_csv[respondent_id]['Duration'] = (
                    respondents[respondent_id - 1].finishTime - respondents[respondent_id - 1].startTime).seconds

        true_id = respondents[respondent_id - 1].id

        # respondent_idは辞書用の詰めた番号、true_idは本当のrespondentのid
        store_question_data(data_to_csv, question_texts, respondent_id, true_id)

    return data_to_csv


def download_csv(request):
    if "enquete_id" not in request.session:
        return redirect("login")
    enquete_id = request.session["enquete_id"]
    enquete = Enquete.objects.get(id=int(enquete_id))

    # enquete = get_object_or_404(Enquete, unique_url=unique_url)
    respondents = Respondent.objects.filter(enquete=enquete)
    questions = Question.objects.filter(enquete=enquete)

    data_to_csv = make_data_to_csv(respondents, questions)
    json_to_csv = json.dumps(data_to_csv, ensure_ascii=False, indent=4, separators=(',', ': '), cls=DjangoJSONEncoder)

    return send_csv_from_json(json_to_csv)
