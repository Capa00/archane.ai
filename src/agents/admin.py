from django.contrib import admin
from django.db.models import JSONField
from django_json_widget.widgets import JSONEditorWidget

from agents.models import Agent
from goal_generation.models import GoalGeneration

class BaseAdmin(admin.ModelAdmin):
    formfield_overrides = {
        JSONField: {'widget': JSONEditorWidget},
    }

class GoalGenerationInline(admin.StackedInline):  # Puoi usare anche StackedInline
    model = GoalGeneration
    max_num = 1

class AgentAdmin(BaseAdmin):
    list_display = ("name",)
    search_fields = ("name",)
    list_filter = ("name",)
    inlines = [GoalGenerationInline]

admin.site.register(Agent, AgentAdmin)
