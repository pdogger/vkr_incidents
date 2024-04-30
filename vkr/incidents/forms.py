from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User

from .models import Basis, Incident, IncidentBasis, IncidentCritery, IncidentExpert, Critery, Strategy


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Имя пользователя', label_suffix="",
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Пароль', label_suffix="",
                               widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'password']


class IncidentForm(forms.ModelForm):
    criteries_list = forms.ModelMultipleChoiceField(
        queryset = Critery.objects.all(),
        widget = forms.CheckboxSelectMultiple,
        required = True
    )

    class Meta:
        model = Incident
        fields = ['name', 'description']


class IncidentExpertForm(forms.ModelForm):
    class Meta:
        model = IncidentExpert
        fields = ['expert']


ExpertFormSet = forms.inlineformset_factory(
    Incident,
    IncidentExpert,
    form=IncidentExpertForm,
    extra=1,
    max_num=6,
    can_delete=False,
    validate_max=True
)


class BasisForm(forms.ModelForm):
    class Meta:
        model = Basis
        fields = ['name', 'description']


BasisFormSet = forms.formset_factory(
    BasisForm,
    extra=0,
    can_delete=False,
    min_num=1,
    validate_min=True,
    max_num=7,
    validate_max=True
)


class StrategyForm(forms.ModelForm):
    class Meta:
        model = Strategy
        fields = ['name', 'description']


StrategyFormSet = forms.formset_factory(
    StrategyForm,
    extra=0,
    can_delete=False,
    min_num=2,
    validate_min=True,
    max_num=7,
    validate_max=True
)
