import json
import copy
import pyminizip
import uuid
from collections import OrderedDict

import yaml
from django.conf import settings
from django.core.files.storage import default_storage
from django.http import HttpResponse
from django.views import generic
import logging
from django.utils.translation import gettext

from AIST_survey.models.enquete import Enquete
from AIST_survey.models.question import Question
from make_enquete_setting.forms import ImportSettingForm


class IndexView(generic.FormView):
    template_name = "make_enquete_setting/index.html"
    form_class = ImportSettingForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # 回答種別の説明文を要求された言語に変換
        type_dict = copy.deepcopy(Question.type_dict)
        for key, value in type_dict.items():
            value['description'] = gettext(value['description'])

        context['question_type'] = json.dumps(type_dict)
        context['password_min_length'] = Enquete.PASSWORD_MIN_LENGTH
        context['password_max_length'] = Enquete.PASSWORD_MAX_LENGTH
        context['title_max_length'] = Enquete._meta.get_field("title").max_length

        # フロントエンド側にDEBUGであるかどうかの値を送信
        context['is_debug'] = settings.DEBUG
        return context

    def post(self, request, *args, **kwargs):
        # YAMLのインポート時にOrderedDictで読み込むための設定
        def construct_odict(loader, node):
            return OrderedDict(loader.construct_pairs(node))

        logger = logging.getLogger('development')
        context = self.get_context_data(**kwargs)
        # 設定ファイルがインポートされた場合はYAMLファイルをパースして渡す
        form = ImportSettingForm(request.POST, request.FILES)
        upload_file = request.FILES['file']
        if form.is_valid():
            file_name = default_storage.save(str(uuid.uuid4()) + ".yaml", upload_file)
            with default_storage.open(file_name) as rf:
                yaml.add_constructor('tag:yaml.org,2002:map', construct_odict)
                setting_data = yaml.safe_load(rf)
            context["setting_data"] = json.dumps(setting_data)

            logger.debug("import_setting : " + str(setting_data))
            default_storage.delete(file_name)
        else:
            context["form_data"] = form
            context["import_error"] = 'インポートしようとしたファイルの形式が不正です。'

        return self.render_to_response(context)


class ExportSettingView(generic.View):
    @staticmethod
    def post(request):
        # yamlをdumpする際にOrderedDictの出力形式を指定する関数
        def represent_odict(dumper, instance):
            return dumper.represent_mapping('tag:yaml.org,2002:map', instance.items())

        # アンケートの設定の入力を取得
        logger = logging.getLogger('development')
        hashed_enquete_password = Enquete.hash_password(request.POST["enquete_password"])
        dic = OrderedDict(enquete_title=request.POST["enquete_title"],
                          enquete_has_password=request.POST["enquete_has_password"],
                          enquete_password=hashed_enquete_password,
                          enquete_published_at=request.POST["enquete_published_at"],
                          enquete_expired_at=request.POST["enquete_expired_at"],
                          # enquete_finished_at=request.POST["enquete_finished_at"],
                          enquete_term_of_service=request.POST["term_of_service"],
                          question_list=[])

        # 質問のリストを取得
        question_text_list = request.POST.getlist("question_text")
        question_type_list = request.POST.getlist("question_type")
        question_is_skip_allowed_list = request.POST.getlist("question_is_skip_allowed")
        question_min_like_required_list = request.POST.getlist("question_min_like_required")
        question_example_answer_list = request.POST.getlist("question_example_answer")
        question_with_answered_num = request.POST.getlist("question_with_answered_num")
        question_without_select = request.POST.getlist("question_without_select")
        question_is_result_public = request.POST.getlist("question_is_result_public")
        for index, question_text in enumerate(question_text_list):
            tmp_dic = OrderedDict(question_text=question_text,
                                  question_type=question_type_list[index],
                                  question_is_skip_allowed=question_is_skip_allowed_list[index],
                                  question_min_like_required=question_min_like_required_list[index],
                                  question_example_answer=question_example_answer_list[index],
                                  question_with_answered_num=question_with_answered_num[index],
                                  question_without_select=question_without_select[index],
                                  question_is_result_public=question_is_result_public[index],
                                  choice_list=request.POST.getlist("choice_text_" + str(index)))
            dic['question_list'].append(tmp_dic)

        logger.debug("export_setting_data : " + str(dic))
        # OrderedDictをdumpする際の出力形式を指定
        # 参考URL：https://qiita.com/podhmo/items/aa954ee1dc1747252436#jsonと互換性をもたせた表現で出力するようにするdictの数値のkeyを文字列にする
        yaml.add_representer(OrderedDict, represent_odict)
        setting_yaml = yaml.dump(dic, default_flow_style=False, allow_unicode=True, encoding="utf-8").decode('utf-8')
        yaml_path = 'export_setting/' + 'enquete_setting_' + str(uuid.uuid4().hex) + '.yaml'
        # YAML設定ファイルを一時ファイルとして保存
        with default_storage.open(yaml_path, 'w') as f:
            f.write(setting_yaml)

        # YAMLファイルを圧縮したzipファイルを一時ファイルとして保存
        zip_path = 'export_setting/' + str(uuid.uuid4()) + '.zip'
        pyminizip.compress(default_storage.path(yaml_path), '/', default_storage.path(zip_path),
                           request.POST["zip_password"], 0)
        # zipファイルからbytesオブジェクトを生成
        string_io = default_storage.open(zip_path, 'rb')
        # 一時ファイル群を削除
        default_storage.delete(yaml_path)
        default_storage.delete(zip_path)

        response = HttpResponse(string_io, content_type='application/zip')
        response['Content-Disposition'] = 'attachment; filename="enquete_setting.zip"'

        return response
