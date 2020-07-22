from AIST_survey.models import *


def get_assessment(is_selected):
    if is_selected:
        return Evaluation.LIKED
    else:
        return Evaluation.PRESENTED


def add_answer(enquete_id, answer_list, respondent_data, ip):
    answer_respondent = Respondent(enquete_id=enquete_id, startTime=respondent_data['startTime'],
                                   hashedIpAddress=Respondent.hash_ip_address(ip))
    answer_respondent.save()

    for answer_id, answer in answer_list.items():
        answer_question = Question.objects.get(pk=int(answer_id))

        if answer_question.type == Question.USERID:
            answer_respondent.attribute = answer['answer']
            answer_respondent.save()
        elif answer_question.type == Question.SINGLE:
            Evaluation.objects.create(respondent=answer_respondent, choice_id=int(answer['answer']),
                                      like=1, assessment=Evaluation.LIKED)
        elif answer_question.type == Question.QUESTION:
            # 選択された回答のデータを追加
            if len(answer['answer']['list']) > 0:
                for i in answer['answer']['list']:
                    Evaluation.objects.create(
                        respondent=answer_respondent, choice_id=int(i['key']),
                        like=1, assessment=get_assessment(i['isSelected'])
                    )
            # 自由回答のデータを追加
            if len(answer['answer']['free']) > 0:
                for i in answer['answer']['free']:
                    new_choice = Choice.objects.create(question=answer_question, text=i)
                    Evaluation.objects.create(
                        respondent=answer_respondent, choice=new_choice, like=1, assessment=Evaluation.PROPOSED
                    )
        elif answer_question.type == Question.MULTI:
            if len(answer['answer']) > 0:
                for i in answer['answer']:
                    Evaluation.objects.create(respondent=answer_respondent, choice_id=int(i),
                                              like=1, assessment=Evaluation.LIKED)


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip
