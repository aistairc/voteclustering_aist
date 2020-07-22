from django.urls import path

from .views import *

app_name = 'make_enquete_setting'
urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('export/', ExportSettingView.as_view(), name='export'),
]
