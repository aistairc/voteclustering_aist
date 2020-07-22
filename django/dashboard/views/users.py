from collections import OrderedDict

from django.shortcuts import redirect, render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.conf import settings

from AIST_survey.models import Enquete, Question, Choice, Respondent, Evaluation


def users(request):
    if "enquete_id" not in request.session:
        return redirect("login")
    enquete_id = request.session["enquete_id"]
    enquete = Enquete.objects.get(id=int(enquete_id))
    params = get_users_params(enquete, request)
    return render(request, 'dashboard/users.html', params)


def get_users_params(enquete, request):
    questions = Question.objects.filter(enquete_id=enquete.id)
    choices = []
    for q in questions:
        choice_data = Choice.objects.filter(question_id=q.id)
        choices.extend(choice_data)

    params = {
        'page_obj': get_user_table_data(enquete, request)
    }
    return params


def get_user_table_data(enquete, request):
    id_serial = 1
    user_table_data = []
    questions = Question.objects.filter(enquete_id=enquete.id)
    respondents = Respondent.objects.filter(enquete_id=enquete.id)
    hashed_ip_dict = OrderedDict()
    for respondent in respondents:
        choice_eval, open_end_eval = get_evaluation_data(respondent.id, questions)
        if respondent.hashedIpAddress in hashed_ip_dict.keys():
            hashed_ip_dict[respondent.hashedIpAddress] += 1
        else:
            hashed_ip_dict[respondent.hashedIpAddress] = 1

        ip_address_id = list(hashed_ip_dict.keys()).index(respondent.hashedIpAddress) + 1
        attribute = respondent.attribute
        user_table_data.append(
            UserTableRow(
                id_serial, respondent, choice_eval, open_end_eval,
                ip_address_id,
                hashed_ip_dict[respondent.hashedIpAddress],
                attribute
            )
        )
        id_serial += 1

    page_obj = paginate_query(request, user_table_data, settings.ITEMS_PER_PAGE)

    return page_obj


# ページネーション用に、Pageオブジェクトを返す。
def paginate_query(request, queryset, count):
    paginator = Paginator(queryset, count)
    page = request.GET.get('page')
    try:
        page_obj = paginator.page(page)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)
    return page_obj



def get_evaluation_data(respondent_id, questions):
    choice_eval = []
    open_end_eval = []
    question_id = 0
    for question in questions:
        if question.type == "single" or question.type == "multi":
            evaluations = Evaluation.objects \
                .filter(choice__question=question, respondent_id=respondent_id, assessment=Evaluation.LIKED)
            for evaluation in evaluations:
                choice = Choice.objects.get(evaluation=evaluation)
                choice_eval.append(f"{question_id}. {choice.text}")
        elif question.type == "question":
            evaluations = Evaluation.objects \
                .filter(choice__question=question, respondent_id=respondent_id, assessment=Evaluation.PROPOSED)
            for evaluation in evaluations:
                choice = Choice.objects.get(evaluation=evaluation)
                open_end_eval.append(f"{question_id}. {choice.text}")
        question_id += 1
    return choice_eval, open_end_eval


class UserTableRow:
    def __init__(self, row_id, respondent, choice_eval, open_end_eval, ip_address_id, num_ip, attribute):
        self.id = row_id
        self.respondent_id = respondent.id
        self.start_time = respondent.startTime
        self.required_time = (respondent.finishTime - respondent.startTime)
        self.choice_eval = choice_eval
        self.open_end_eval = open_end_eval
        self.ip_address_id = ip_address_id
        self.num_ip = num_ip
        self.attribute = attribute

