from django.contrib import admin
from .models import GoalGeneration

@admin.register(GoalGeneration)
class GoalGenerationAdmin(admin.ModelAdmin):
    list_display = ("name",)  # Personalizza le colonne visibili nella lista admin
    search_fields = ("name",)  # Aggiunge la ricerca nei campi
