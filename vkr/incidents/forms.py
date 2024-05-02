from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User

from .models import Incident, Basis, IncidentExpert, Criteria, Strategy


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
        queryset=Criteria.objects.all(),
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'mt-1'}),
        required=True,
        label="Критерии",
    )

    class Meta:
        model = Incident
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control mt-1'}),
            'description': forms.Textarea(attrs={'class': 'form-control mt-1'})
        }


ExpertFormSet = forms.inlineformset_factory(
    Incident,
    IncidentExpert,
    fields=['expert'],
    widgets = {'expert': forms.Select(attrs={'class': 'form-select-sm'})},
    extra=0,
    can_delete=False
)


BasisFormSet = forms.inlineformset_factory(
    Incident,
    Basis,
    fields=['name', 'description'],
    widgets = {'name': forms.TextInput(attrs={'class': 'form-control mt-1'}),
               'description': forms.Textarea(attrs={'class': 'form-control mt-1',
                                                    'rows': 5})},
    extra=0,
    can_delete=False,
    min_num=1,
    validate_min=True,
    max_num=7,
    validate_max=True
)


StrategyFormSet = forms.inlineformset_factory(
    Incident,
    Strategy,
    fields=['name', 'description'],
    widgets = {'name': forms.TextInput(attrs={'class': 'form-control mt-1'}),
               'description': forms.Textarea(attrs={'class': 'form-control mt-1',
                                                    'rows': 5})},
    extra=0,
    can_delete=False,
    min_num=2,
    validate_min=True,
    max_num=5,
    validate_max=True
)
