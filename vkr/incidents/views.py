import datetime
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.http import Http404, HttpResponseRedirect
from django.contrib.auth.forms import AuthenticationForm

from .models import Incident, Expert, IncidentExpert
from .forms import IncidentCreateForm
from .utils.calculate import calculate_incident, check_all_experts_done, get_all_scores


def signin(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            return redirect('index')

        form = AuthenticationForm()
        return render(request, 'incidents/login.html', {'form': form})

    elif request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('incidents')

        print(dir(form))
        return render(request, 'incidents/login.html', {'form': form})


@login_required(login_url='login')
def index(request):
    return redirect('incidents')


@login_required(login_url='login')
def incidents_list(request):
    incidents = Incident.objects.all()
    return render(request, "incidents/incidents.html", {
            'incidents': incidents})


@login_required(login_url='login')
def incident_create(request):
    if request.method == 'POST':
        form_incident = IncidentCreateForm(request.POST)
        if form_incident.is_valid():
            creator, _ = Expert.objects.get_or_create(user_id=request.user.id)
            incident = Incident.objects.create(
                name=form_incident.cleaned_data['name'],
                description=form_incident.cleaned_data['description'],
                creator_id=creator, status_id=1,
                created_at=datetime.datetime.now()
            )
            return HttpResponseRedirect(f"/incident?incident_id={incident.id}")

    else:
        form_incident = IncidentCreateForm()

    return render(request, "incidents/incident_create.html", {"form_incident": form_incident})

def incident_delete(request):
    incident_id = request.DELETE['incident_id']
    try:
        Incident.objects.get(id=incident_id).delete()
    except Incident.DoesNotExist:
        raise Http404("Инцидент не существует")
    return render(request, "incidents/incident_delete.html")

@login_required(login_url='login')
def incident(request, incident_id):
    if request.method == 'GET':
        try:
            incident = Incident.objects.get(id=incident_id)
        except Incident.DoesNotExist:
            raise Http404("Инцидент не существует")
        return render(request, "incidents/incident.html", {
            'incident': incident})
    if request.method == 'DELETE':
        return incident_delete(request)

# Несуществующая форма пока что
def incident_assessment(request):
    if request.method == 'POST':
        form_inc_assessment = IncidentAssessmentForm(request.POST)
        if form_inc_assessment.is_valid():

            expert_id = request.user.id
            incident_id = request.POST['incident_id']

            try:
                incident = Incident.objects.get(id=incident_id)
            except Incident.DoesNotExist:
                raise Http404("Инцидент не существует")

            try:
                Expert.objects.get(id=expert_id)
            except Expert.DoesNotExist:
                raise Http404("Эксперт не существует")

            incident_expert = IncidentExpert.objects.get(incident_id=incident_id,
                                                         expert_id=expert_id)
            incident_expert.scores = form_inc_assessment.cleaned_data['scores']
            incident_expert.save()

            if check_all_experts_done(incident):
                incident.status = "Оценен"
                incident.results = calculate_incident(get_all_scores(incident))
                incident.save()

            return HttpResponseRedirect(f"/incident?incident_id={incident_id}")

    else:
        form_inc_assessment = IncidentAssessmentForm()

    return render(request, "incidents/incident_assessment.html",
                  {"form_inc_assessment": form_inc_assessment})

@login_required(login_url='login')
def examples(request):
    if request.method == 'GET':
        return render(request, "incidents/examples.html")

@login_required(login_url='login')
def methods(request):
    if request.method == 'GET':
        return render(request, "incidents/methods.html")