from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User

from .models import Expert


class IncidentCreateForm(forms.Form):
    name = forms.CharField(label="Название инцидента", max_length=100)
    description = forms.CharField(label="Описание инцидента", widget=forms.Textarea)

    experts = forms.ModelMultipleChoiceField(Expert.objects, widget=forms.CheckboxSelectMultiple)


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Имя пользователя', label_suffix="",
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Пароль', label_suffix="",
                               widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'password']
