from django import forms
from django.contrib import admin
from django.db.models import JSONField
from django_json_widget.widgets import JSONEditorWidget
from django_jsonform.widgets import JSONFormWidget
import nested_admin

from .models import Module, Action, ModuleAction, Execution


class JSONWidgetAdminMixin:
    formfield_overrides = {
        JSONField: {'widget': JSONEditorWidget},
    }


# Form custom per ModuleAction che usa django-jsonform per il campo config
class ModuleActionForm(forms.ModelForm):
    class Meta:
        model = ModuleAction
        fields = '__all__'
        # Di default si imposta JSONFormWidget per il campo config
        widgets = {
            'config': JSONFormWidget(schema={}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Se è presente l'istanza e l'azione associata, utilizza lo schema definito in Action.config_schema
        if self.instance and getattr(self.instance, 'action', None):
            self.fields['config'].widget = JSONFormWidget(
                schema=self.instance.action.config_schema or {}
            )
        else:
            self.fields['config'].widget = JSONFormWidget(schema={})


# Inline per Execution, usato all'interno dell'inline di ModuleAction
class ExecutionInline(JSONWidgetAdminMixin, nested_admin.NestedStackedInline):
    model = Execution
    extra = 0
    fields = ('started_at', 'finished_at', 'inputs', 'config', 'output')
    readonly_fields = ('started_at', 'finished_at', 'output')
    show_change_link = True


# Inline per ModuleAction da visualizzare nella pagina del Module
class ModuleActionInlineForModule(nested_admin.NestedStackedInline):
    model = ModuleAction
    form = ModuleActionForm
    extra = 0
    show_change_link = True


# Inline per ModuleAction da visualizzare nella pagina dell'Action
class ModuleActionInlineForAction(nested_admin.NestedStackedInline):
    model = ModuleAction
    form = ModuleActionForm
    extra = 0
    fields = ('module', 'order', 'config')
    show_change_link = True


@admin.register(Module)
class ModuleAdmin(JSONWidgetAdminMixin, nested_admin.NestedModelAdmin):
    list_display = ('name', 'created_at')
    search_fields = ('name',)
    ordering = ('name',)
    inlines = [ModuleActionInlineForModule]


@admin.register(Action)
class ActionAdmin(JSONWidgetAdminMixin, nested_admin.NestedModelAdmin):
    list_display = ('name', 'funcname', 'created_at')
    search_fields = ('name',)
    ordering = ('name',)
    # inlines = [ModuleActionInlineForAction]


@admin.register(ModuleAction)
class ModuleActionAdmin(JSONWidgetAdminMixin, admin.ModelAdmin):
    form = ModuleActionForm
    list_display = ('module', 'action')
    list_filter = ('module', 'action')
    search_fields = ('module', 'action')
    ordering = ('module', 'order')


@admin.register(Execution)
class ExecutionAdmin(JSONWidgetAdminMixin, admin.ModelAdmin):
    list_display = ('module_action', 'started_at', 'finished_at')
    list_filter = ('module_action',)
    search_fields = ('module_action__module_name', 'module_action__funcname')
    ordering = ('-started_at',)
