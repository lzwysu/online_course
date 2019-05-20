from django.urls import path,re_path
from django.views.generic import TemplateView
from .views import *

app_name = 'organization'

urlpatterns = [
    path('org_list/', OrgView.as_view(), name='org_list'),
]