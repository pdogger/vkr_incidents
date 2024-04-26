from django.contrib import admin

from .models import Basis, Critery, Expert, Incident, Status, Strategy

admin.site.register(Basis)
admin.site.register(Critery)
admin.site.register(Expert)
admin.site.register(Incident)
admin.site.register(Status)
admin.site.register(Strategy)
