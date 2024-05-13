import json

from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.db.models import Case, Count, When
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.utils import timezone

from .forms import (
    AssessmentForm,
    BasisFormSet,
    ExpertFormSet,
    IncidentForm,
    LoginUserForm,
    SolutionForm,
    StrategyFormSet,
)
from .models import Expert, Incident, IncidentExpert, Status, Strategy
from .utils.calculate import calculate_incident, get_all_scores, prepare_scores
from .utils.prepare_data import dict_decode, dict_encode, prepare_results


def signin(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            return redirect('index')

        form = LoginUserForm()
        return render(request, 'incidents/login.html', {'form': form})

    elif request.method == 'POST':
        form = LoginUserForm(request, data=request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('incidents')

        return render(request, 'incidents/login.html', {'form': form})


@login_required(login_url='login')
def incidents_list(request) -> HttpResponse:
    incidents = Incident.objects.all().annotate(
        is_expert=Count(Case(When(experts__user=request.user, then=1))),
    ).order_by('-is_expert', 'status', '-created_at')

    return render(request, "incidents/incidents.html", {"incidents": incidents})


@login_required(login_url='login')
def incident_create(request) -> HttpResponseRedirect | HttpResponse:
    if request.method == 'GET':
        incident_form = IncidentForm()
        expert_formset = ExpertFormSet()
        basis_formset = BasisFormSet()
        strategy_formset = StrategyFormSet()
    elif request.method == 'POST':
        incident_form = IncidentForm(request.POST)
        expert_formset = ExpertFormSet(request.POST)
        basis_formset = BasisFormSet(request.POST)
        strategy_formset = StrategyFormSet(request.POST)

        if all([
            incident_form.is_valid(), expert_formset.is_valid(),
            basis_formset.is_valid(), strategy_formset.is_valid(),
        ]):
            incident = incident_form.save(commit=False)
            incident.created_at = timezone.now()
            incident.creator = Expert.objects.get(user=request.user)
            incident.status = Status.objects.get(name="Инициирован")
            incident.save()

            criteries = incident_form.cleaned_data['criteries_list']
            for num, criteria in enumerate(criteries):
                incident.incidentcriteria_set.create(criteria=criteria, number=num + 1)

            IncidentExpert.objects.create(
                incident=incident,
                expert=incident.creator,
                number=1,
            )
            experts_related = expert_formset.save(commit=False)
            experts_related = filter(
                lambda x: x.expert.user != incident.creator.user,
                experts_related,
            )
            for num, expert in enumerate(experts_related):
                expert.number = num + 2
                expert.incident = incident
                expert.save()

            basises_related = basis_formset.save(commit=False)
            for num, basis in enumerate(basises_related):
                basis.number = num + 1
                basis.incident = incident
                basis.save()

            strategies_related = strategy_formset.save(commit=False)
            for num, strategy in enumerate(strategies_related):
                strategy.number = num + 1
                strategy.incident = incident
                strategy.save()

            return redirect('incident', incident_id=incident.id)
    return render(
        request, 'incidents/incident_create.html',
        {
            'incident_form': incident_form, 'expert_formset': expert_formset,
            'basis_formset': basis_formset, 'strategy_formset': strategy_formset,
        },
    )


@login_required(login_url='login')
def incident_delete(request, incident_id):
    if request.method == 'POST':
        try:
            Incident.objects.get(id=incident_id).delete()
        except Incident.DoesNotExist:
            raise Http404("Инцидент не существует")
        return redirect("incidents")


@login_required(login_url='login')
def incident(request, incident_id):
    if request.method == 'GET':
        try:
            incident = Incident.objects.get(id=incident_id)
        except Incident.DoesNotExist:
            raise Http404("Инцидент не существует")

        try:
            expert = Expert.objects.get(user=request.user)
        except Expert.DoesNotExist:
            raise Http404("Эксперт не существует")

        experts_with_scores = IncidentExpert.objects.filter(
            incident=incident,
            scores__isnull=False,
        )
        incident_expert = IncidentExpert.objects.filter(
            incident=incident,
            expert=expert,
        ).first()
        results = prepare_results(incident)

        for expert in experts_with_scores:
            expert.scores = dict_decode(expert.scores)

        solution_form = SolutionForm(choices=incident.strategy_set.all())
        return render(
            request, "incidents/incident.html", {
                'incident': incident,
                'incident_expert': incident_expert,
                'is_active': (incident.status.name not in ('Решен', 'Отклонен')),
                'solution_form': solution_form,
                'experts_with_scores': experts_with_scores,
                'results': results,
            },
        )


@login_required(login_url='login')
def incident_assess(request, incident_id):
    if request.method == 'POST':
        try:
            incident = Incident.objects.get(id=incident_id)
        except Incident.DoesNotExist:
            raise Http404("Инцидент не существует")

        try:
            expert = Expert.objects.get(user=request.user)
        except Expert.DoesNotExist:
            raise Http404("Эксперт не существует")

        experts = IncidentExpert.objects.filter(incident=incident).all().order_by('number')

        done = True
        for expert_m in experts:
            if expert_m.expert_id == expert.id:
                incident_expert = expert_m
                incident_expert.scores = dict_encode(
                    prepare_scores(
                        json.loads(request.body),
                        incident.criteries.count(),
                        incident.strategy_set.count(),
                    ),
                )
                incident_expert.save()
            if expert_m.scores is None:
                done = False

        if done:
            incident.status = Status.objects.get(name="Оценен")
            incident.results = dict_encode(calculate_incident(get_all_scores(experts)))
            incident.save()
        elif incident.status.name == 'Инициирован':
            incident.status = Status.objects.get(name="В процессе оценивания")
            incident.save()

        return HttpResponse(status=200)

    else:
        try:
            incident = Incident.objects.get(id=incident_id)
        except Incident.DoesNotExist:
            raise Http404("Инцидент не существует")
        criteries = incident.criteries.all()
        basises = incident.basis_set.all()
        strategies = incident.strategy_set.all()
        assessment_form = AssessmentForm()
        return render(
            request, "incidents/incident_assess.html",
            {
                'incident': incident, 'assessment_form': assessment_form,
                'criteries': criteries, 'basises': basises, 'strategies': strategies,
            },
        )


@login_required(login_url='login')
def incident_solved(request, incident_id):
    if request.method == "POST":
        try:
            incident = Incident.objects.get(id=incident_id)
        except Incident.DoesNotExist:
            raise Http404("Инцидент не существует")

        strategy_number = int(json.loads(request.body)) + 1
        strategy = Strategy.objects.filter(incident=incident_id, number=strategy_number).first()
        if strategy is None:
            incident.status = Status.objects.get(name='Отклонен')
            incident.save()
        else:
            print(strategy.incident)
            strategy.is_solution = True
            strategy.save()
            incident.status = Status.objects.get(name='Решен')
            incident.save()

        return HttpResponse(status=200)


@login_required(login_url='login')
def examples(request):
    if request.method == 'GET':
        return render(request, "incidents/examples.html")


@login_required(login_url='login')
def methods(request):
    if request.method == 'GET':
        return render(request, "incidents/methods.html")
