from django.contrib.auth import password_validation
from django.contrib.auth.hashers import (
    check_password, make_password,
)
from django.db import models
from django.utils.crypto import get_random_string
import secrets


class Enquete(models.Model):
    UNIQUE_URL_LENGTH = 5
    ACCESS_TOKEN_BYTE_LENGTH = 20
    # passwordはハッシュ化した値が保存される都合上、フィールドの引数で文字数制限ができないため定数を指定
    PASSWORD_MIN_LENGTH = 5
    PASSWORD_MAX_LENGTH = 20

    title = models.CharField(max_length=255)
    has_password = models.BooleanField(default=False)
    password = models.CharField(max_length=128, blank=True, null=True)
    # URLに用いる一意の文字列．今後の運用次第で10字まで可能にしておく．
    unique_url = models.CharField(max_length=10, unique=True)
    # Dashboardのログイン時の認証に使用する一意な文字列
    access_token = models.CharField(max_length=60, unique=True, blank=True, null=True)
    published_at = models.DateTimeField()
    expired_at = models.DateTimeField(blank=True, null=True)
    # expired_atがNULLでなくfinished_atがNULLの場合、finished_atにexpired_atの値が入るようsave()にて設定している
    finished_at = models.DateTimeField(blank=True, null=True)
    term_of_service = models.TextField()

    """
    以下の処理はdjango.contrib.auth.base_user内のAbstractBaseUserクラスを参考にしている
    予めハッシュ化したパスワードをを直接DBに追加する、パスワードを利用しないことがあるなどAbstractBaseUserと比べて特殊な操作が多いため継承を行っていない
    参照：https://github.com/django/django/blob/master/django/contrib/auth/base_user.py
    """

    # Stores the raw password if set_password() is called so that it can
    # be passed to password_changed() after the model is saved.
    # set_hashed_passwordが呼び出された場合は生のパスワードではなくハッシュ後のパスワードが保存される
    _password = None

    def set_password(self, raw_password):
        self.password = make_password(raw_password)
        self._password = raw_password

    def save(self, *args, **kwargs):
        # unique_url, access_tokenが存在しない場合は生成
        if len(self.unique_url) == 0:
            self.unique_url = self.generate_unique_url()
        if self.access_token is None:
            self.access_token = self.generate_access_token()

        # 公開期限日が設定されていない場合、回答期限日と同一であると設定
        if self.expired_at and not self.finished_at:
            self.finished_at = self.expired_at
        super().save(*args, **kwargs)
        if self._password is not None:
            password_validation.password_changed(self._password, self)
            self._password = None

    # 一意かつ紛らわしい文字列を除いた，ランダムな英小文字を生成
    def generate_unique_url(self):
        while True:
            unique_url = get_random_string(length=self.UNIQUE_URL_LENGTH, allowed_chars='cefghjkmnprstwx')
            if Enquete.objects.filter(unique_url=unique_url).exists():
                continue
            else:
                break
        return unique_url

    # 一意なアクセストークンを生成する
    def generate_access_token(self):
        while True:
            token = secrets.token_hex(self.ACCESS_TOKEN_BYTE_LENGTH)
            if Enquete.objects.filter(access_token=token).exists():
                continue
            else:
                break
        return token

    # 引数のトークンと一致するEnqueteを返す
    # 一致するEnqueteが存在しない場合はNoneを返す
    # secrets.compare_digestはタイミング攻撃のリスクを減らす方法で比較を行うため==ではなくこちらでの比較を推奨
    @staticmethod
    def compare_access_token(token):
        matched_enquete = next(
            filter((lambda x: secrets.compare_digest(token, x.access_token) if (x.access_token is not None) else False), Enquete.objects.all()),
            None
        )
        return matched_enquete

    @staticmethod
    def hash_password(raw_password):
        return make_password(raw_password)

    def set_hashed_password(self, hashed_password):
        # この関数ではハッシュ前の生のパスワードが取得不能のためハッシュ後のパスワードを_passwordに保存している
        # 確認した範囲では問題なさそうだが問題を確認した場合は修正が必要
        _password = hashed_password
        self.password = hashed_password

    def check_password(self, raw_password):
        """
        Return a boolean of whether the raw_password was correct. Handles
        hashing formats behind the scenes.
        """

        def setter(raw_password):
            self.set_password(raw_password)
            # Password hash upgrades shouldn't be considered password changes.
            self._password = None
            self.save(update_fields=["password"])

        return check_password(raw_password, self.password, setter)

    def __str__(self):
        return self.title
