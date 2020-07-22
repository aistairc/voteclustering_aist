from django.test import TestCase
from AIST_survey.models import Enquete

from datetime import datetime, timezone, timedelta
from django import db
from django.utils.crypto import get_random_string

JST = timezone(timedelta(hours=+9), 'JST')


class EnqueteModelTests(TestCase):
    def test_is_empty(self):
        saved_enquetes = Enquete.objects.all()
        self.assertEquals(saved_enquetes.count(), 0)

    def test_creating_enquete(self):
        self.create_enquete()

        saved_enquete = Enquete.objects.all()
        self.assertEquals(saved_enquete.count(), 1)

    def create_enquete(self, title="Test", has_password=True, password="Test", term_url="Test",
                       published_at=datetime.now(JST), expired_at=datetime.now(JST) + timedelta(days=1)):
        enquete = Enquete()

        enquete.title = title
        enquete.has_password = has_password
        enquete.set_hashed_password(Enquete.hash_password(password))
        enquete.term_url = term_url
        enquete.unique_url = get_random_string(length=5, allowed_chars='cefghjkmnprstwx')
        enquete.published_at = published_at
        enquete.expired_at = expired_at

        enquete.save()

        return enquete

    # 正しくハッシュ化できているかを確認
    def test_check_password(self):
        password = 'Test'
        enquete = EnqueteModelTests().create_enquete(password=password)

        self.assertTrue(enquete.check_password(password))

    # 255文字を超える入力でエラーが出るか
    def test_title_field(self):
        with self.assertRaises(db.DataError):
            self.create_enquete(title="aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
                                  "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
                                  "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
                                  "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
                                  "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
