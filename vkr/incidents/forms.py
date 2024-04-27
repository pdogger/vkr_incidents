from django import forms

from .models import Expert


class IncidentCreateForm(forms.Form):
    name = forms.CharField(label="Название инцидента", max_length=100)
    description = forms.CharField(label="Описание инцидента", widget=forms.Textarea)

    experts = forms.ModelMultipleChoiceField(Expert.objects, widget=forms.CheckboxSelectMultiple)
