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


class AssessmentForm(forms.Form):
    CHOICES = {'1/9': 'Очень сильно уступает (1/9)',
               '1/7': 'Значительно уступает (1/7)',
               '1/5': 'Сильно уступает (1/5)',
               '1/3': 'Умеренно уступает (1/3)',
               '1': 'Варианты равноценны (1)',
               '3': 'Умеренно превосходит (3)',
               '5': 'Сильно превосходит (5)',
               '7': 'Значительно превосходит (7)',
               '9': 'Очень сильно превосходит (9)'}
    choice = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-select-sm'}),
                          choices=CHOICES, initial='1')


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


class SolutionForm(forms.Form):
    choice = forms.ChoiceField(
        label="Пожалуйста, укажите стратегию, позволившую устранить инцидент",
        widget=forms.RadioSelect(attrs={'class': 'form-select-sm mb-2'})
    )

    def __init__(self, *args, choices=None, **kwargs):
        super().__init__(*args, **kwargs)
        if choices is not None:
            self.fields['choice'].choices = [(choice.number - 1, choice.name) \
                for choice in choices] + [(len(choices), 'Инцидент не был решен')]


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
