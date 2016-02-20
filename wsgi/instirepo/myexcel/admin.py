from django.contrib import admin
from django.forms import Textarea
from myexcel.models import *


class ChoiceInline(admin.TabularInline):
    model = Details
    extra = 1


class WorksAdmin(admin.ModelAdmin):
    inlines = [ChoiceInline]
    list_display = ('tool_number', 'jw_number', 'product', 'date', 'target_date', 'status', 'remarks')
    formfield_overrides = {
        models.TextField: {'widget': Textarea(
            attrs={'rows': 4,
                   'cols': 90, })},
    }


class DetailsAdmin(admin.ModelAdmin):
    list_display = ('date', 'trial_date', 'action_taken', 'status', 'remarks')
    formfield_overrides = {
        models.TextField: {'widget': Textarea(
            attrs={'rows': 4,
                   'cols': 90, })},
    }


admin.site.register(Works, WorksAdmin)
admin.site.register(Details, DetailsAdmin)
