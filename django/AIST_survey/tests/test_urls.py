from django.test import TestCase
from .test_enquete_model import EnqueteModelTests


class URLTests(TestCase):
    # 正しいHTMLを表示できるかのテスト
    def test_index_view(self):
        enquete = EnqueteModelTests().create_enquete()
        response = self.client.get('/AIST_survey/{}/'.format(enquete.unique_url))
        self.assertEquals(response.template_name[0], 'AIST_survey/index.html')
