from django import forms
from django.contrib import admin, messages
from django.db.models import JSONField
from django.http import HttpResponseRedirect
from django.urls import path, reverse
from django_json_widget.widgets import JSONEditorWidget
from django_jsonform.widgets import JSONFormWidget
import nested_admin

from agents.models import Agent
from .models import Module, Action, ModuleAction, Execution
from django.utils.translation import gettext_lazy as _


class JSONWidgetAdminMixin:
    formfield_overrides = {
        JSONField: {'widget': JSONEditorWidget},
    }


class ModuleAdminForm(forms.ModelForm):
    agents = forms.ModelMultipleChoiceField(
        queryset=Agent.objects.all(),
        widget=admin.widgets.FilteredSelectMultiple("Agents", is_stacked=False),
        required=False
    )

    class Meta:
        model = Module
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['agents'].initial = self.instance.agents.all()

    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            instance.save()
        if instance.pk:
            instance.agents.set(self.cleaned_data['agents'])  # Aggiorna gli agenti associati
        return instance

# Form custom per ModuleAction che usa django-jsonform per il campo config
class ModuleActionForm(forms.ModelForm):
    class Meta:
        model = ModuleAction
        fields = '__all__'
        # Di default si imposta JSONFormWidget per il campo config
        widgets = {
            'config': JSONFormWidget(schema={}),
            'input': JSONFormWidget(schema={}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Se è presente l'istanza e l'azione associata, utilizza lo schema definito in Action.config_schema
        if self.instance and getattr(self.instance, 'action', None):
            self.fields['configs'].widget = JSONFormWidget(schema=self.instance.action.config_schema or {})
            self.fields['inputs'].widget = JSONFormWidget(schema=self.instance.action.input_schema or {})
        else:
            self.fields['configs'].widget = JSONFormWidget(schema={})
            self.fields['inputs'].widget = JSONFormWidget(schema={})


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


class AgentInline(admin.StackedInline):
    model = Module.agents.through
    extra = 0


@admin.register(Module)
class ModuleAdminNestedInline(JSONWidgetAdminMixin, admin.ModelAdmin):
    list_display = ('name', 'created_at')
    search_fields = ('name',)
    ordering = ('name',)
    form = ModuleAdminForm
    inlines = [AgentInline, ModuleActionInlineForModule]


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
    list_filter = ('module__name', 'action__funcname', 'action__name')
    search_fields = ('module', 'action')
    ordering = ('module', 'order')

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                '<int:moduleaction_id>/execute/',
                self.admin_site.admin_view(self.execute_action),
                name='moduleaction_execute',
            ),
        ]
        return custom_urls + urls

    def execute_action(self, request, *args, moduleaction_id=None, **kwargs):
        """
        View per eseguire l'azione associata a questo ModuleAction.
        In questo esempio creiamo un record di Execution e lo eseguiamo.
        """
        module_action = self.get_object(request, moduleaction_id)
        if not module_action:
            messages.error(request, _("ModuleAction non trovato."))
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/admin/'))

        execution = module_action.execute(module_action.inputs, module_action.configs, request.user)
        messages.success(
            request,
            f"Azione eseguita con successo"
        )

        return HttpResponseRedirect(
            reverse("admin:modules_execution_change", args=[execution.id])
        )

    def change_view(self, request, object_id, form_url='', extra_context=None):
        """
        Iniettiamo nel contesto del template una variabile object_tools,
        contenente il link al nostro tool per eseguire l'azione.
        """
        extra_context = extra_context or {}
        extra_context['object_tools'] = [
            {
                'url': reverse('admin:moduleaction_execute', args=[object_id]),
                'label': 'Esegui Azione',
                'class': 'button',
                'icon': 'fa-play',
                'wait': True,
            }
        ]
        return super().change_view(request, object_id, form_url, extra_context=extra_context)


@admin.register(Execution)
class ExecutionAdmin(JSONWidgetAdminMixin, admin.ModelAdmin):
    list_display = ('module_action', 'started_at', 'finished_at')
    list_filter = ('module_action',)
    search_fields = ('module_action__module_name', 'module_action__funcname')
    ordering = ('-started_at',)
