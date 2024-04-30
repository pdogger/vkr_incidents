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

class BasisAdmin(admin.ModelAdmin):
    list_display = ('name', 'id', 'incident')
    search_fields = ['name', 'description']


class CriteriaAdmin(admin.ModelAdmin):
    list_display = ('description', 'id')
    search_fields = ['description']


class ExpertAdmin(admin.ModelAdmin):
    list_display = ('user', 'fullname', 'id')
    search_fields = ['user__username']

    def fullname(self, obj):
        return obj.user.get_full_name()


class IncidentCriteriaAdmin(admin.ModelAdmin):
    list_display = ('incident', 'criteria', 'number')
    search_fields = ['incident__name']


class IncidentExpertAdmin(admin.ModelAdmin):
    list_display = ('incident', 'expert', 'number')
    search_fields = ['incident__name']


class StatusAdmin(admin.ModelAdmin):
    list_display = ('name', 'id')


class StrategyAdmin(admin.ModelAdmin):
    list_display = ('name', 'id', 'incident')
    search_fields = ['name', 'description']


class IncidentAdmin(admin.ModelAdmin):
    list_display = ('name', 'id', 'creator', 'created_at', 'status')
    search_fields = ['name', 'description']
    inlines = [BasisInline, CriteriaInline, ExpertInline, StrategyInline]


admin.site.register(Basis, BasisAdmin)
admin.site.register(Criteria, CriteriaAdmin)
admin.site.register(Expert, ExpertAdmin)
admin.site.register(Incident, IncidentAdmin)
admin.site.register(IncidentCriteria, IncidentCriteriaAdmin)
admin.site.register(IncidentExpert, IncidentExpertAdmin)
admin.site.register(Status, StatusAdmin)
admin.site.register(Strategy, StrategyAdmin)
