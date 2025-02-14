from django.contrib import admin

from modules.admin.mixins import JSONWidgetAdminMixin
from modules.forms.module_action_admin_form import ModuleActionForm
from modules.forms.module_admin_form import ModuleAdminForm
from modules.models import Module, ModuleAction


# class AgentInline(admin.StackedInline):
#     model = Module.agents.through
#     extra = 1

class ModuleActionInlineForModule(admin.StackedInline):
    model = ModuleAction
    form = ModuleActionForm
    extra = 0
    show_change_link = True


@admin.register(Module)
class ModuleAdmin(JSONWidgetAdminMixin, admin.ModelAdmin):
    list_display = ('name', 'created_at')
    list_filter = ('agents',)
    search_fields = ('name',)
    ordering = ('name',)
    form = ModuleAdminForm
    inlines = [ModuleActionInlineForModule]