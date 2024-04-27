from django import forms
from django.forms import ModelForm


class IncidentCreateForm(forms.Form):
    name = forms.CharField(label="Название инцидента", max_length=100)
    description = forms.CharField(label="Описание инцидента", widget=forms.Textarea)
