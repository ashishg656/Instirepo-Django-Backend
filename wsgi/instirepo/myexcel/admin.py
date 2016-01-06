from django.contrib import admin
from myexcel.models import *


class ChoiceInline(admin.TabularInline):
    model = Details
    extra = 3


class WorksAdmin(admin.ModelAdmin):
    inlines = [ChoiceInline]
    list_display = ('tool_number', 'jw_number', 'product', 'date', 'target_date', 'status', 'remarks')


class DetailsAdmin(admin.ModelAdmin):
    list_display = ('date', 'trial_date', 'action_taken', 'status', 'remarks')


admin.site.register(Works, WorksAdmin)
admin.site.register(Details, DetailsAdmin)
