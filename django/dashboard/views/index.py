from django.db.models import Count, Q
from django.shortcuts import redirect, render
from django.utils import timezone

from AIST_survey.models import Enquete, Respondent, Question, Choice, Evaluation


def index(request):
    if "enquete_id" not in request.session:
        return redirect("login")
    enquete_id = request.session["enquete_id"]
    enquete = Enquete.objects.get(id=int(enquete_id))

    params = get_index_params(enquete)
    return render(request, 'dashboard/index.html', params)


def get_index_params(enquete):
    respondents = Respondent.objects.filter(enquete_id=enquete.id)
    questions = Question.objects.filter(enquete_id=enquete.id)
    choices = []
    for q in questions:
        choice_data = Choice.objects.filter(question_id=q.id)
        choices.extend(choice_data)
    params = {
        'enquete': enquete,
        'respondent_num': len(respondents),
        'today_respondents_num': get_today_respondents_num(enquete),
        'remaining_days': get_remaining_days(enquete),
        'respondent_transition_data': get_respondent_transition_data(enquete),
        'question_graph_data': get_question_graph_data(enquete)
    }
    return params


def get_question_graph_data(enquete):
    questions = Question.objects.filter(enquete_id=enquete.id)
    graph_data = []
    for q in questions:
        if q.type == Question.SINGLE or q.type == Question.MULTI:
            data = {
                "question_text": q.text,
                "type": "selection",
                "graph_data": get_selection_data(q)
            }
            graph_data.append(data)
        elif q.type == Question.QUESTION:
            data = {
                "question_text": q.text,
                "type": "open_end",
                "graph_data": get_question_data(q)
            }
            graph_data.append(data)
    return graph_data


def get_selection_data(question):
    choices = Choice.objects.filter(question=question)
    selection_labels = []
    selection_data = []
    for c in choices:
        choice_num = Evaluation.objects.filter(choice=c).count()
        selection_labels.append(c.text)
        selection_data.append(choice_num)
    return {"labels": selection_labels, "data": selection_data}


def get_question_data(question):
    choices = Choice.objects.filter(question=question)
    question_data = {
        "like": [],
        "time": [],
    }
    choices_timestamp = choices.order_by("-timestamp")[0:5]
    for choice in choices_timestamp:
        question_data["time"].append({
            "time": choice.timestamp,
            "text": choice.text
        })
    choices_like = choices\
        .annotate(
            count=Count(
                "evaluation",
                filter=Q(evaluation__assessment=Evaluation.LIKED) | Q(evaluation__assessment=Evaluation.PROPOSED)
            )
        )\
        .order_by("-count")[0:5]
    for choice in choices_like:
        question_data["like"].append({
            "text": choice.text,
            "like": choice.count,
            "timestamp": choice.timestamp
        })
    return question_data


def get_today_respondents_num(enquete):
    today_respondents = Respondent.objects.filter(enquete_id=enquete.id, finishTime__date=timezone.now())
    return today_respondents.count()


def get_remaining_days(enquete):
    remaining_days = (enquete.expired_at - timezone.now()).days
    return remaining_days if remaining_days > 0 else 0


def get_respondent_transition_data(enquete):
    today = timezone.now().date()
    date_list = []
    respondent_count_list = []
    publish_day = enquete.published_at.astimezone().replace(hour=23, minute=59, second=59, microsecond=999999)
    while publish_day.date() <= today:
        respondent_count = Respondent.objects.filter(finishTime__date__lte=publish_day, enquete_id=enquete.id).count()
        date_list.append(publish_day.strftime("%Y/%m/%d"))
        respondent_count_list.append(respondent_count)
        publish_day += timezone.timedelta(days=1)
    return {'labels': date_list, 'values': respondent_count_list}
