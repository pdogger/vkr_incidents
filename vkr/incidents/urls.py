from django.urls import path, reverse_lazy
from django.contrib.auth.views import LogoutView

from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("incident", views.incident, name="incident"),
    path("incidents", views.incidents_list, name="incidents_get"),
    path("incident/create", views.incident_create, name="incident_create"),
    path("login", views.signin, name="login"),
    path("logout", LogoutView.as_view(), name="logout"),
]
