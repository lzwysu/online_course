from django import forms
from operation.models import UserAsk
from django.db import models


class UserAskForm(forms.ModelForm):
    '''我要咨询'''
    class Meta:
        model = UserAsk
        fields = ['name','mobile','course_name']