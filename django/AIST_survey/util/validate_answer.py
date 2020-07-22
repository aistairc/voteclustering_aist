from AIST_survey.models import *
from AIST_survey.util.add_answer import get_assessment
import logging
import sys
from django.core.exceptions import ValidationError


class ValidateAnswer:
    def __init__(self, enquete_id, answer_list):
        self.enquete_id = enquete_id
        self.answer_list = answer_list

    # 特定のアンケートに対して引数の回答データがすべてアンケートの質問が要求する事項を満たしているか確認する関数
    def validate_answer(self):
        logger = logging.getLogger("development")
        logger.debug("---------validate answer------------")
        logger.debug(str(self.answer_list))

        question_list = Question.objects.filter(enquete_id=self.enquete_id)
        for answer_question in question_list:
            question_is_valid, message = self.__validate_question(answer_question)
            if not question_is_valid:
                logger.debug(message)
                return False, message

        return True, ""

    def __validate_question(self, answer_question):
        is_valid, message = \
            self.__is_valid_skip_question(answer_question.id, answer_question.is_skip_allowed, answer_question.text)
        if not is_valid:
            return False, message

        if str(answer_question.id) not in self.answer_list:
            return True, ""

        question_data = self.answer_list[str(answer_question.id)]

        is_valid, message = self.__is_valid_question_type(question_data, answer_question)
        if not is_valid:
            return False, message

        is_valid, message = self.__is_valid_question(question_data, answer_question)
        if not is_valid:
            return False, message

        return True, ""

    def __is_valid_skip_question(self, question_id, is_skip_allowed, question_text):
        if is_skip_allowed or question_id in self.answer_list:
            return True, ""
        else:
            return False, f"[Question:{question_text}] Question data is not exist in query."

    @staticmethod
    def __is_valid_question_type(question_data, answer_question):
        if "type" not in question_data:
            return False, f"[Question:{answer_question.text}] Query does not have question type."
        if question_data["type"] != answer_question.type:
            return False, f"[Question:{answer_question.text} type:{answer_question.type}]" \
                f" Type in your request ({question_data['type']}) does not match."
        return True, ""

    def __is_valid_question(self, question_data, answer_question):
        if "key" not in question_data:
            return False, f"[Question:{answer_question.text}] Query does not have question key."

        if answer_question.type == Question.USERID:
            return self.__is_valid_user_id_question(question_data, answer_question)
        elif answer_question.type == Question.SINGLE:
            return self.__is_valid_single_question(question_data, answer_question)
        elif answer_question.type == Question.MULTI:
            return self.__is_valid_multi_question(question_data, answer_question)
        elif answer_question.type == Question.QUESTION:
            return self.__is_valid_question_question(question_data, answer_question)
        else:
            return False, f"invalid question type: {answer_question.type}"

    @staticmethod
    def __is_valid_user_id_question(question_data, answer_question):
        if "answer" not in question_data:
            return False, f"[Question:{answer_question.text}] Query does not have property 'answer'."
        if len(question_data["answer"]) == 0:
            return False, f"[Question:{answer_question.text}] Length of 'answer' is 0."
        return True, ""

    @staticmethod
    def __is_valid_single_question(question_data, answer_question):
        if "answer" not in question_data:
            return False, f"[Question:{answer_question.text}] Query does not have property 'answer'."
        try:
            Evaluation(respondent=None, choice_id=int(question_data['answer']), like=1, assessment=Evaluation.LIKED) \
                .full_clean(exclude=['respondent'])
        except ValidationError as e:
            ex, ms, tb = sys.exc_info()
            return False, str(ms)
        return True, ""

    @staticmethod
    def __is_valid_multi_question(question_data, answer_question):
        if "answer" not in question_data:
            return False, f"[Question:{answer_question.text}] Query does not have property 'answer'."
        if len(question_data["answer"]) <= 0:
            return False, f"[Question:{answer_question.text}] Query does not have content of property 'answer'."
        for i in question_data["answer"]:
            try:
                Evaluation(respondent=None, choice_id=int(i), like=1, assessment=Evaluation.LIKED)\
                    .full_clean(exclude=['respondent'])
            except ValidationError as e:
                ex, ms, tb = sys.exc_info()
                return False, str(ms)
        return True, ""

    @staticmethod
    def __is_valid_question_question(question_data, answer_question):
        if "answer" not in question_data:
            return False, f"[Question:{answer_question.text}] Query does not have property 'answer'."
        if "list" in question_data["answer"]:
            for i in question_data["answer"]["list"]:
                if "key" not in i:
                    return False, f"[Question:{answer_question.text}] Query does not have choice key in 'answer'."
                if "isSelected" not in i:
                    return False, f"[Question:{answer_question.text}] Query does not have isSelected in 'answer'."
                try:
                    Evaluation(
                        respondent=None, choice_id=int(i['key']),
                        like=1, assessment=get_assessment(i['isSelected'])
                    ).full_clean(exclude=['respondent'])
                except ValidationError:
                    ex, ms, tb = sys.exc_info()
                    return False, str(ms)
        if "free" in question_data["answer"]:
            try:
                Choice(question_id=question_data["key"], text=question_data["answer"]["free"]).full_clean()
                Evaluation(respondent=None, choice=None, like=1, assessment=Evaluation.PROPOSED)\
                    .full_clean(exclude=["respondent", "choice"])
            except ValidationError:
                ex, ms, tb = sys.exc_info()
                return False, str(ms)
        return True, ""
