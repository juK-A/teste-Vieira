from django.contrib import admin
from .models import Responsible, Activities

class ResponsibleAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

class ActivitiesAdmin(admin.ModelAdmin):
    list_display = ('name_activity', 'owner', 'responsible', 'done', 'created_at', 'deleted_at', 'deleted_by', 'due_date')
    list_filter = ('done', 'owner', 'responsible')
    search_fields = ('name_activity', 'description')

admin.site.register(Responsible, ResponsibleAdmin)
admin.site.register(Activities, ActivitiesAdmin)