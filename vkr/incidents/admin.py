from django.contrib import admin

from .models import (
    Basis,
    Critery,
    Expert,
    Incident,
    IncidentBasis,
    IncidentCritery,
    IncidentExpert,
    IncidentStrategy,
    Status,
    Strategy
)


class BasisInline(admin.TabularInline):
    model = IncidentBasis
    extra = 1


class CriteryInline(admin.TabularInline):
    model = IncidentCritery
    extra = 1


class ExpertInline(admin.TabularInline):
    model = IncidentExpert
    extra = 1


class StrategyInline(admin.TabularInline):
    model = IncidentStrategy
    extra = 1


class IncidentAdmin(admin.ModelAdmin):
    inlines = [BasisInline, CriteryInline, ExpertInline, StrategyInline]


admin.site.register(Basis)
admin.site.register(Critery)
admin.site.register(Expert)
admin.site.register(Incident, IncidentAdmin)
admin.site.register(Status)
admin.site.register(Strategy)
