from django.contrib import admin, messages
from django.http import HttpResponseRedirect
from django.urls import path, reverse
from django.utils.translation import gettext_lazy as _

from modules.admin import JSONWidgetAdminMixin
from modules.forms.module_action_admin_form import ModuleActionForm
from modules.models import ModuleAction


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