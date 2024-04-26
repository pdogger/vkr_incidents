from django.shortcuts import render
from django.http import Http404
from .models import Incident


def index(request):
    return render(request, "base.html")

def incidents_list(request):
    incidents = Incident.objects.all()
    return render(request, "incidents.html", {
            'incidents': incidents})

def incident_create(request):
    pass

def incident(request):
    if request.method == 'GET':
        incident_id = request.GET['incident_id']
        try:
            incident = Incident.objects.get(id=incident_id)
        except Incident.DoesNotExist:
            raise Http404("Incident does not exist")
        return render(request, "incident.html", {
            'incident': incident})
