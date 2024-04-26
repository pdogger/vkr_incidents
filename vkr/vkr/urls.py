from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("incidents/", include("incidents.urls")),
    path('admin/', admin.site.urls),
]
