#coding:utf-8
__author__ = 'lquterqtd'
from django import forms
from django.contrib.admin import widgets
########################################################################
class ReportDateSelectForm(forms.Form):
    """"""
    StartDate = forms.DateTimeField(required=True, label='起始日期', widget=widgets.AdminDateWidget())
    EndDate = forms.DateTimeField(required=True, label='终止日期', widget=widgets.AdminDateWidget())