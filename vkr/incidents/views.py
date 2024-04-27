from django.shortcuts import render
from django.http import Http404, HttpResponseRedirect
from .models import Incident, Expert, IncidentExpert
from django.views.decorators.csrf import csrf_exempt
from .forms import IncidentCreateForm
import datetime
from django.forms import modelformset_factory
from .calculate import calculate_incident


def check_all_experts_done(incident: Incident) -> bool:
    for e in incident.experts.all():
        if IncidentExpert.objects.filter(incident_id=incident.id, expert_id=e.id, scores__isnull = True).count() > 0:
            return False
    return True

def get_all_scores(incident: Incident) -> list:
    scores = []

    # TODO упорядочить по номеру эксперта
    for e in incident.experts.all():
        scores.append(IncidentExpert.objects.get(incident_id=incident.id, expert_id=e.id).scores)
    return scores


def index(request):
    return render(request, "base.html")

def incidents_list(request):
    incidents = Incident.objects.all()
    return render(request, "incidents.html", {
            'incidents': incidents})

def incident_create(request):
    if request.method == 'POST':
        form_incident = IncidentCreateForm(request.POST)
        if form_incident.is_valid():
            creator, _ = Expert.objects.get_or_create(user_id=request.user.id)
            incident = Incident.objects.create(name=form_incident.cleaned_data['name'],
                                                description=form_incident.cleaned_data['description'],
                                                  creator_id=creator, status_id=1,
                                                    created_at=datetime.datetime.now())
            return HttpResponseRedirect(f"/incident?incident_id={incident.id}")
    
    else:
        form_incident = IncidentCreateForm()

    return render(request, "incident_create.html", {"form_incident": form_incident})

def incident_delete(request):
    incident_id = request.DELETE['incident_id']
    try:
        Incident.objects.get(id=incident_id).delete()
    except Incident.DoesNotExist:
        raise Http404("Инцидент не существует")
    return render(request, "incident_delete.html")

def incident(request):
    if request.method == 'GET':
        incident_id = request.GET['incident_id']
        try:
            incident = Incident.objects.get(id=incident_id)
        except Incident.DoesNotExist:
            raise Http404("Инцидент не существует")
        return render(request, "incident.html", {
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
            
            incident_expert = IncidentExpert.objects.get(incident_id=incident_id, expert_id=expert_id)
            incident_expert.scores = form_inc_assessment.cleaned_data['scores']
            incident_expert.save()

            if check_all_experts_done(incident):
                incident.status = "Оценен"
                incident.results = calculate_incident(get_all_scores(incident))
                incident.save()

            return HttpResponseRedirect(f"/incident?incident_id={incident_id}")
    
    else:
        form_inc_assessment = IncidentAssessmentForm()

    return render(request, "incident_assessment.html", {"form_inc_assessment": form_inc_assessment})
