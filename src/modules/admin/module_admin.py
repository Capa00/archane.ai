from django.contrib import admin, messages

from modules.admin.mixins import JSONWidgetAdminMixin, ExternalSchemaBasedInlineAdminMixin
from modules.forms.module_admin_form import ModuleAdminForm
from modules.models import Module, ModuleAction


# class AgentInline(admin.StackedInline):
#     model = Module.agents.through
#     extra = 1
@admin.action(description="Duplica i Module selezionati")
def duplicate_module(modeladmin, request, queryset):
    for agent in queryset:
        agent.duplicate()
    messages.success(request, "I Module sono stati duplicati con successo!")


class ModuleActionInlineForModule(ExternalSchemaBasedInlineAdminMixin, admin.StackedInline):
    model = ModuleAction
    #form = ModuleActionForm
    extra = 0
    show_change_link = True

    external_schemas_mapping = {
        "action.input_schema": "inputs",
        "action.config_schema": "configs",
    }


@admin.register(Module)
class ModuleAdmin(JSONWidgetAdminMixin, admin.ModelAdmin):
    actions = [duplicate_module]
    list_display = ('name', 'description', 'created_at')
    list_filter = ('agents',)
    search_fields = ('name',)
    ordering = ('name',)
    form = ModuleAdminForm
    inlines = [ModuleActionInlineForModule]