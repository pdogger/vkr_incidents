from django.contrib.auth.views import LogoutView
from django.urls import path, reverse_lazy
from django.views.generic.base import RedirectView

from . import views


urlpatterns = [
    path("", RedirectView.as_view(url=reverse_lazy('incidents')), name="index"),
    path("incident/<int:incident_id>", views.incident, name="incident"),
    path("incidents", views.incidents_list, name="incidents"),
    path("incident/create", views.incident_create, name="incident_create"),
    path("incident/assess/<int:incident_id>", views.incident_assess, name="incident_assess"),
    path("incident/delete/<int:incident_id>", views.incident_delete, name="incident_delete"),
    path("login", views.signin, name="login"),
    path("logout", LogoutView.as_view(), name="logout"),
    path("examples", views.examples, name="examples"),
    path("methods", views.methods, name="methods"),
]
