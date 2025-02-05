from django.contrib import admin

from agents.admin import ModuleAdmin
from .models import GoalGeneration

@admin.register(GoalGeneration)
class GoalGenerationAdmin(ModuleAdmin):
    list_display = ("name", "agent__name")  # Personalizza le colonne visibili nella lista admin
    search_fields = ("name",)  # Aggiunge la ricerca nei campi
    list_filter = ("agent", )

    fieldsets = (
        ("Configurazione Agente", {
            "fields": ("agent",),
            #"classes": ("collapse",),
        }),
        ("Informazioni Generali", {
            "fields": ("name", "system_prompt"),
            #"classes": ("collapse",),  # Rende la sezione collassabile
        }),
        ("Data", {
            "fields": ("data",),
            "classes": ("collapse",),
        }),
        ("Data Schema", {
            "fields": ("data_schema",),
            "classes": ("collapse",),
        }),
        ("Last Output", {
            "fields": ("output",),
            "classes": ("collapse",),
        }),
        ("Output Schema", {
            "fields": ("output_schema",),
            "classes": ("collapse",),
        }),
    )