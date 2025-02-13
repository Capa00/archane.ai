from django.contrib import admin

from modules.admin import JSONWidgetAdminMixin
from modules.models import Execution


@admin.register(Execution)
class ExecutionAdmin(JSONWidgetAdminMixin, admin.ModelAdmin):
    list_display = ('module_action', 'started_at', 'finished_at')
    list_filter = ('module_action',)
    search_fields = ('module_action__module_name', 'module_action__funcname')
    ordering = ('-started_at',)