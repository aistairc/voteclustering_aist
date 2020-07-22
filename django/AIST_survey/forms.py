import yaml
from django import forms

from AIST_survey.models.enquete import Enquete


class UploadForm(forms.Form):
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


class PasswordForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput, label='新しいパスワード')

    def clean_password(self):
        password = self.cleaned_data['password']
        if not Enquete.PASSWORD_MIN_LENGTH <= len(password) <= Enquete.PASSWORD_MAX_LENGTH:
            raise forms.ValidationError('パスワードは5文字以上20文字以下に設定してください')

        return password
