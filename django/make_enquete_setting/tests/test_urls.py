from django.test import TestCase


class URLTests(TestCase):
    # 正しいHTMLを表示できるかのテスト
    def test_index_view(self):
        response = self.client.get('/make_enquete_setting/')
        self.assertEquals(response.template_name[0], 'make_enquete_setting/index.html')

    # 200が返ってくることをテスト
    def test_export_view(self):
        test_data = {
            'csrfmiddlewaretoken': ['lwurZtKqfJEKGsh7d9tZihbLbwktHnTah4cCUS6skmX3lADszUsnyO7htMY0DzQp'],
            'enquete_title': ['保健室の利用に関するアンケート'],
            'enquete_has_password': ['true'],
            'enquete_password': ['fdafsa'],
            'enquete_term_url': ['enquete_tp://example.com'],
            'enquete_published_at': ['2014/03/15 05:06'],
            'enquete_expired_at': ['2014/03/15 05:06'],
            'enquete_finished_at': ['2014/03/15 05:06'],
            'question_text': ['保健室を利用した理由を教えてください'],
            'question_type': ['question_with_opinion'],
            'question_is_skip_allowed': ['true'],
            'question_min_like_required': ['0'],
            'question_example_answer': ['けがをしたため'],
            'question_with_answered_num': ['true'],
            'question_without_select': ['true'],
            'choice_list': [],
            'zip_password': ['dfasad']
        }
        response = self.client.post('/make_enquete_setting/export/', data=test_data)

        self.assertEquals(response.status_code, 200)
