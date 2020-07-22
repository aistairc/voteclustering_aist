from django.urls import path

from .views import *

app_name = 'AIST_survey'
urlpatterns = [
    path('enquete/<str:unique_url>/', IndexView.as_view(), name='index'),
    # path('lite_enquete/<str:unique_url>/', LiteIndexView.as_view(), name='lite_index'),
    path('ajax/ajax_check_password', ajax.ajax_check_password, name='check_password'),
    path('ajax/ajax_get_others_opinion', ajax.ajax_get_others_opinion, name='get_others_opinion'),
    path('ajax/ajax_add_answer', ajax.ajax_add_answer, name='add_answer'),
    path('ajax/ajax_suggest', ajax.ajax_suggest, name='suggest'),
    path('template/question/<str:unique_url>', QuestionTemplateView.as_view(), name='question_template'),
    path('template/top', TopTemplateView.as_view(), name='top_template'),
]
