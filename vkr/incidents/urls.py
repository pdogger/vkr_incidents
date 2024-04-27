from django.urls import path

from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("incident", views.incident, name="incident"),
    path("incidents", views.incidents_list, name="incidents_get"),
    path("incident/create", views.incident_create, name="incident_create"),
    path("login", views.signin, name="login")
]
