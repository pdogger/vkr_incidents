from django.contrib import admin

from .models import (
    Basis,
    Criteria,
    Expert,
    Incident,
    IncidentCriteria,
    IncidentExpert,
    Status,
    Strategy
)


class BasisInline(admin.TabularInline):
    model = Basis
    extra = 1


class CriteriaInline(admin.TabularInline):
    model = IncidentCriteria
    extra = 1


class ExpertInline(admin.TabularInline):
    model = IncidentExpert
    extra = 1


class StrategyInline(admin.TabularInline):
    model = Strategy
    extra = 1


class IncidentAdmin(admin.ModelAdmin):
    inlines = [BasisInline, CriteriaInline, ExpertInline, StrategyInline]


admin.site.register(Basis)
admin.site.register(IncidentCriteria)
admin.site.register(IncidentExpert)
admin.site.register(Strategy)
admin.site.register(Criteria)
admin.site.register(Expert)
admin.site.register(Incident, IncidentAdmin)
admin.site.register(Status)
