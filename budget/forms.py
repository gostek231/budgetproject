from django import forms
import datetime


class ExpenseForm(forms.Form):
    title = forms.CharField()
    amount = forms.IntegerField()
    category = forms.CharField()
    date = forms.DateField()