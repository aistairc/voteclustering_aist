# -*- coding: utf-8 -*-
from collections import OrderedDict

from django.core.serializers.python import Serializer as JSONSerializer


# モデルの要素をJSON形式で出力するためのシリアライザ
class Serializer(JSONSerializer):
    # django.core.serializers.python.Serializerのget_dump_objectをオーバーライドし必要なフィールドを抽出
    def get_dump_object(self, obj):
        data = OrderedDict()
        # Questionモデルのidを取得
        if not self.use_natural_primary_keys or not hasattr(obj, 'natural_key'):
            data["id"] = self._value_from_field(obj, obj._meta.pk)
        # Questionモデルの各フィールドの要素を取得
        data.update(self._current)
        return data
