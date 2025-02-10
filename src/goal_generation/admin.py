from django.contrib import admin, messages
from django.http import JsonResponse
from django.shortcuts import redirect
from django.urls import path, reverse
from django.utils.translation import gettext_lazy as _

from agents.admin import ModuleAdmin
from .models import GoalGeneration

@admin.register(GoalGeneration)
class GoalGenerationAdmin(ModuleAdmin):
    list_display = ("name", "agent__name")  # Personalizza le colonne visibili nella lista admin
    search_fields = ("name",)  # Aggiunge la ricerca nei campi
    list_filter = ("agent", )

    fieldsets = (
        ("Configurazione Agente", {"fields": ("agent",)}),
        ("Informazioni Generali", {"fields": ("name", "system_prompt"),}),
        ("Data", {"fields": ("data",), "classes": ("collapse",),}),
        ("Data Schema", {"fields": ("data_schema",), "classes": ("collapse",),}),
        ("Last Output", {"fields": ("output",), "classes": ("collapse",),}),
        ("Output Schema", {"fields": ("output_schema",), "classes": ("collapse",),}),
    )

    def get_urls(self):
        """Aggiunge una URL per eseguire make_output direttamente dalla change view."""
        urls = super().get_urls()
        custom_urls = [
            path('<int:pk>/run-make-output/', self.admin_site.admin_view(self.run_make_output), name='goal_generation_make_output'),
        ]
        return custom_urls + urls

    def run_make_output(self, request, pk):
        obj = self.get_queryset(request).get(pk=pk)
        try:
            obj.make_output()  # Esegue la funzione make_output
            obj.save()
            self.message_user(request, "make_output eseguito con successo!", messages.SUCCESS)
        except Exception as e:
            self.message_user(request, f"Errore: {e}", messages.ERROR)

        redirect_url = request.META.get(
            'HTTP_REFERER',
            reverse("admin:goal_generation_goalgeneration_change", args=[pk])
        )
        # Se la richiesta è AJAX, restituisco il JSON con l'URL di redirect.
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'redirect_url': redirect_url})
        return redirect(redirect_url)

    def change_view(self, request, object_id, form_url='', extra_context=None):
        """Aggiunge il pulsante alla pagina di modifica."""
        extra_context = extra_context or {}
        extra_context["object_tools"] = [
            {
                "url": reverse('admin:goal_generation_make_output', args=[object_id]),
                "label": _("Genera Output"),
                "icon": "fa-play",
                "class": "button",
                "wait": True  # Il tool attende il completamento della richiesta AJAX
            },
        ]

        return super().change_view(request, object_id, form_url, extra_context=extra_context)