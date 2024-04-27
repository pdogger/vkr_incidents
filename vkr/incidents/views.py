import datetime
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.http import Http404, HttpResponseRedirect
from django.contrib.auth.forms import AuthenticationForm

from .models import Incident, Expert
from .forms import IncidentCreateForm


def signin(request):
    if request.method == 'GET':
        form = AuthenticationForm()
        return render(request, 'login.html', {'form': form})

    elif request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)

                return redirect('index')

        return render(request, 'login.html', {'form': form})


@login_required(login_url='login')
def index(request):
    return render(request, "base.html")


@login_required(login_url='login')
def incidents_list(request):
    incidents = Incident.objects.all()
    return render(request, "incidents.html", {
            'incidents': incidents})


@login_required(login_url='login')
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


@login_required(login_url='login')
def incident(request):
    if request.method == 'GET':
        incident_id = request.GET['incident_id']
        try:
            incident = Incident.objects.get(id=incident_id)
        except Incident.DoesNotExist:
            raise Http404("Incident does not exist")
        return render(request, "incident.html", {
            'incident': incident})
