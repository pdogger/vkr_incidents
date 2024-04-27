from django.shortcuts import render
from django.http import Http404, HttpResponseRedirect
from .models import Incident, Expert
from django.views.decorators.csrf import csrf_exempt
from .forms import IncidentCreateForm
import datetime
from django.forms import modelformset_factory

def index(request):
    return render(request, "base.html")

def incidents_list(request):
    incidents = Incident.objects.all()
    return render(request, "incidents.html", {
            'incidents': incidents})

def incident_create(request):
    ExpertFormSet = modelformset_factory(Expert, fields=["user"], max_num=7, extra=7)
    if request.method == 'POST':
        form_incident = IncidentCreateForm(request.POST)
        expert_formset = ExpertFormSet(request.POST)
        if form_incident.is_valid() and expert_formset.is_valid():
            creator, _ = Expert.objects.get_or_create(user_id=request.user.id)
            incident = Incident.objects.create(name=form_incident.cleaned_data['name'],
                                                description=form_incident.cleaned_data['description'],
                                                  creator_id=creator, status_id=1,
                                                    created_at=datetime.datetime.now())
            return HttpResponseRedirect(f"/incident?incident_id={incident.id}")
    
    else:
        form_incident = IncidentCreateForm()
        expert_formset = ExpertFormSet()

    return render(request, "incident_create.html", {"form_incident": form_incident, "expert_formset": expert_formset})

def incident(request):
    if request.method == 'GET':
        incident_id = request.GET['incident_id']
        try:
            incident = Incident.objects.get(id=incident_id)
        except Incident.DoesNotExist:
            raise Http404("Incident does not exist")
        return render(request, "incident.html", {
            'incident': incident})
