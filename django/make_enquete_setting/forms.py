import yaml
from django import forms


class ImportSettingForm(forms.Form):
    file = forms.FileField(label='ファイル')

    def clean_file(self):
        file = self.cleaned_data['file']
        # ファイルの拡張子がYAMLであることを確認
        if not file.name.endswith('.yaml'):
            raise forms.ValidationError('アップロード可能な拡張子は.yamlのみです')

        # ロードを行いファイルが正常なYAMLファイルかをチェック
        try:
            yaml.safe_load(file)
        except yaml.YAMLError:
            raise forms.ValidationError('ファイルのエンコーディングや正しいYAMLファイルかを確認してください')

        return file
