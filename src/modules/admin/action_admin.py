from django.contrib import admin

from modules.admin import JSONWidgetAdminMixin
from modules.models import Action


@admin.register(Action)
class ActionAdmin(JSONWidgetAdminMixin, admin.ModelAdmin):
    list_display = ('name', 'funcname', 'created_at')
    list_filter = ('name', 'funcname')
    search_fields = ('name',)
    ordering = ('name',)
