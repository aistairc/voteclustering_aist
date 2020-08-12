import datetime
import logging
import uuid
from collections import OrderedDict
from distutils.util import strtobool

import yaml
from django.contrib import admin
from django.contrib import messages
from django.core import serializers
from django.core.exceptions import ImproperlyConfigured
from django.core.exceptions import ValidationError
from django.core.files.storage import default_storage
from django.db.models import Q
from django.shortcuts import redirect
from django.shortcuts import render
from django.urls import path
from django.http import HttpResponse

from . import forms
from .models import *


# Register your models here.


class MyListFilter(admin.RelatedFieldListFilter):
    # 必ずフィルタリングを出力
    def has_output(self):
        return True


# 参考URL: https://qiita.com/maisuto/items/e160bb17ef594f3c4d50
class ListFilterFromEnquete(MyListFilter):
    enquete_id_exact = None

    def __init__(self, field, request, params, model, model_admin, field_path):
        super().__init__(field, request, params, model, model_admin, field_path)
        if self.enquete_id_exact is None:
            raise ImproperlyConfigured(
                "The list filter '%s' does not specify a 'enquete_id_exact'."
                % self.__class__.__name__
            )

    def field_choices(self, field, request, model_admin):
        enquete_id = request.GET.get(self.enquete_id_exact)
        limit_choices_to = Q(enquete_id__exact=enquete_id) if enquete_id else None
        return field.get_choices(include_blank=False, limit_choices_to=limit_choices_to)


class ListFilterFromEnqueteForChoice(ListFilterFromEnquete):
    enquete_id_exact = 'question__enquete__id__exact'


class ListFilterFromEnqueteForEvaluation(ListFilterFromEnquete):
    enquete_id_exact = 'choice__question__enquete__id__exact'


class QuestionInline(admin.TabularInline):
    model = Question
    extra = 0


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 0


class EnqueteAdmin(admin.ModelAdmin):
    # 詳細において，階層化
    fieldsets = [
        (None, {'fields': ['title', 'has_password', 'password', 'unique_url', 'access_token', 'term_of_service']}),
        ('Date information', {'fields': ['published_at', 'expired_at', 'finished_at']})
    ]
    # 詳細において，Questionモデルを表示
    inlines = [QuestionInline]
    # 一覧において，作成順にソート
    ordering = ['id']
    # 一覧において，表示する情報
    list_display = (
        'id', 'title', 'has_password', 'unique_url', 'access_token', 'published_at', 'expired_at', 'finished_at')
    list_display_links = ['title']

    # インポート画面をURLから参照できるように設定
    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('import/', self.import_enquete_setting_view),
            path('<path:object_id>/change/password', self.change_password),
            path('<path:object_id>/change/export_json', self.export_model_as_json),
        ]
        return my_urls + urls

    # モデルのエクスポート用View
    def export_model_as_json(self, request, **kwargs):
        enquete_id = kwargs['object_id']
        enquetes = Enquete.objects.filter(id=enquete_id)
        questions = Question.objects.filter(enquete_id=enquete_id)
        question_ids = map(lambda q: q.id, questions)
        choices = Choice.objects.filter(question_id__in=question_ids)
        choice_ids = map(lambda c: c.id, choices)
        respondents = Respondent.objects.filter(enquete_id=enquete_id)
        evaluations = Evaluation.objects.filter(choice_id__in=choice_ids)

        result = list(enquetes) + list(questions) + list(choices) + list(respondents) + list(evaluations)
        result_json = serializers.serialize("json", result)

        response = HttpResponse(result_json, content_type='application/json')
        response['Content-Disposition'] = 'attachment; filename=export.json'
        return response

    # パスワード変更画面のView
    def change_password(self, request, **kwargs):
        enquete_id = kwargs['object_id']

        if request.method == 'POST':
            form = forms.PasswordForm(request.POST)
            if form.is_valid():
                enquete = Enquete.objects.get(id=enquete_id)
                enquete.password = Enquete.hash_password(form.cleaned_data['password'])
                enquete.save()

                messages.success(request, 'パスワードを正常に更新しました')

                return redirect('/admin/AIST_survey/enquete/' + enquete_id)

        form = forms.PasswordForm()

        context = {
            'form': form,
        }

        return render(request, 'admin/AIST_survey/enquete/change_password.html', context=context)

    # インポート設定画面のView
    def import_enquete_setting_view(self, request):
        # YAMLのインポート時にOrderedDictで読み込むための設定
        def construct_odict(loader, node):
            return OrderedDict(loader.construct_pairs(node))

        def format_datetime(datetime_str, nullable):
            # nullを許容するフィールドかつ入力が空文字 or nullならばNoneを返す
            if nullable and not datetime_str:
                return None
            return datetime.datetime.strptime(datetime_str, "%Y/%m/%d %H:%M")

        def str_to_bool(bool_str):
            return bool(strtobool(bool_str))

        def validate_import_setting(input_setting_data):
            try:
                Enquete(title=input_setting_data['enquete_title'],
                        has_password=str_to_bool(input_setting_data['enquete_has_password']),
                        password=input_setting_data['enquete_password'],
                        published_at=format_datetime(input_setting_data['enquete_published_at'],
                                                     nullable=Enquete._meta.get_field("published_at").null),
                        expired_at=format_datetime(input_setting_data['enquete_expired_at'],
                                                   nullable=Enquete._meta.get_field("expired_at").null),
                        # finished_at=format_datetime(input_setting_data['enquete_finished_at'])
                        term_of_service=input_setting_data['enquete_term_of_service'],
                        ).full_clean(exclude=['unique_url', 'access_token'])
                validation_question_setting_list = input_setting_data['question_list']
                for validation_question_setting in validation_question_setting_list:
                    q = Question(
                        enquete=None,
                        type=validation_question_setting['question_type'],
                        text=validation_question_setting['question_text'],
                        is_skip_allowed=str_to_bool(validation_question_setting['question_is_skip_allowed']),
                        min_like_required=validation_question_setting['question_min_like_required'],
                        example_answer=validation_question_setting['question_example_answer']
                    )
                    q.full_clean(exclude=['enquete'])
                    validation_choice_setting_list = validation_question_setting['choice_list']
                    for validation_choice_setting in validation_choice_setting_list:
                        Choice(question=None,
                               text=validation_choice_setting
                               ).full_clean(exclude=['question'])
            except KeyError as e:
                raise ValidationError(str(e) + 'のフィールドが存在しません')
            except ValueError as e:
                raise ValidationError(e)
            except ValidationError as e:
                raise ValidationError(e)

        if request.method == 'POST':
            form = forms.UploadForm(request.POST, request.FILES)
            upload_file = request.FILES['file']
            if form.is_valid():
                file_name = default_storage.save(str(uuid.uuid4()) + ".yaml", upload_file)
                with default_storage.open(file_name) as rf:
                    yaml.add_constructor('tag:yaml.org,2002:map', construct_odict)
                    setting_data = yaml.safe_load(rf)

                logger = logging.getLogger('development')
                logger.debug(setting_data)

                # 設定ファイルがモデルの制約を満たしているかを確認
                try:
                    validate_import_setting(setting_data)
                except ValidationError as error_message:
                    data = {
                        'form': form,
                        'message': '設定ファイルのデータが不正です：' + str(error_message),
                    }
                    default_storage.delete(file_name)
                    return render(request, 'admin/AIST_survey/enquete/import_setting_file.html', data)

                # 設定ファイルの情報をデータベースに追加
                enquete_object = Enquete.objects.create(title=setting_data['enquete_title'],
                                                        has_password=str_to_bool(setting_data['enquete_has_password']),
                                                        password=setting_data['enquete_password'],
                                                        published_at=format_datetime(
                                                            setting_data['enquete_published_at'],
                                                            nullable=Enquete._meta.get_field("published_at").null),
                                                        expired_at=format_datetime(
                                                            setting_data['enquete_expired_at'],
                                                            nullable=Enquete._meta.get_field("expired_at").null),
                                                        # finished_at=format_datetime(setting_data['enquete_finished_at'])
                                                        term_of_service=setting_data['enquete_term_of_service'],
                                                        )
                question_setting_list = setting_data['question_list']
                for question_setting in question_setting_list:
                    question_object = Question.objects.create(enquete=enquete_object,
                                                              type=question_setting['question_type'],
                                                              text=question_setting['question_text'],
                                                              is_skip_allowed=str_to_bool(
                                                                  question_setting['question_is_skip_allowed']),
                                                              min_like_required=question_setting[
                                                                  'question_min_like_required'],
                                                              example_answer=question_setting[
                                                                  'question_example_answer'],
                                                              with_answered_num=str_to_bool(
                                                                  question_setting['question_with_answered_num']),
                                                              without_select=str_to_bool(
                                                                  question_setting['question_without_select']))
                    choice_setting_list = question_setting['choice_list']
                    for choice_setting in choice_setting_list:
                        Choice.objects.create(question=question_object,
                                              text=choice_setting)

                default_storage.delete(file_name)

                return redirect('/admin/AIST_survey/enquete/' + str(enquete_object.id))
            else:
                data = {
                    'form': form,
                    'message': 'アップロードされたファイルが不正です',
                }
                return render(request, 'admin/AIST_survey/enquete/import_setting_file.html', data)
        else:
            form = forms.UploadForm()

        data = {
            'form': form,
            # 'message': message,
        }
        return render(request, 'admin/AIST_survey/enquete/import_setting_file.html', data)


class QuestionAdmin(admin.ModelAdmin):
    fields = ['enquete', 'type', 'text', 'is_skip_allowed', 'min_like_required',
              'example_answer', 'with_answered_num', 'without_select']
    inlines = [ChoiceInline]
    ordering = ['id']
    list_filter = [('enquete', MyListFilter)]
    list_display = ['id', 'enquete', 'type', 'text', 'is_skip_allowed', 'min_like_required',
                    'example_answer', 'with_answered_num', 'without_select']
    list_display_links = ['text']


class ChoiceAdmin(admin.ModelAdmin):
    fields = ['question', 'respondent', 'text', 'timestamp']
    ordering = ['id']
    list_filter = [
        ('question__enquete', MyListFilter),
        ('question', ListFilterFromEnqueteForChoice)
    ]
    list_display = ['id', 'enquete', 'question', 'respondent', 'text', 'timestamp']
    list_display_links = ['text']

    # list_displayに対応したメソッド
    def enquete(self, instance):
        return instance.question.enquete


class EvaluationAdmin(admin.ModelAdmin):
    fields = ['respondent', 'choice', 'like', 'assessment', 'timestamp']
    ordering = ['id']
    list_filter = [
        ('choice__question__enquete', MyListFilter),
        ('choice__question', ListFilterFromEnqueteForEvaluation),
        ('respondent', ListFilterFromEnqueteForEvaluation)
    ]
    list_display = ['id', 'respondent', 'enquete', 'question', 'choice', 'like', 'assessment', 'timestamp']
    list_display_links = ['id', 'like']

    def question(self, instance):
        return instance.choice.question

    def enquete(self, instance):
        return instance.choice.question.enquete


class RespondentAdmin(admin.ModelAdmin):
    fields = ['enquete', 'attribute', 'startTime', 'finishTime', 'hashedIpAddress']
    ordering = ['id']
    list_filter = [('enquete', MyListFilter)]
    list_display = ['id', 'enquete', 'attribute', 'startTime', 'finishTime', 'hashedIpAddress']
    list_display_links = ['id']


admin.site.register(Enquete, EnqueteAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice, ChoiceAdmin)
admin.site.register(Evaluation, EvaluationAdmin)
admin.site.register(Respondent, RespondentAdmin)
