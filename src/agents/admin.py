from django.contrib import admin
from django.db.models import JSONField
from django_json_widget.widgets import JSONEditorWidget

from agents.models import Agent
from goal_generation.models import GoalGeneration
from wizard_form_widget.forms import MyModelForm


# class BaseAdmin(admin.ModelAdmin):
#     formfield_overrides = {
#         JSONField: {'widget': JSONEditorWidget},
#     }
#
# class GoalGenerationInline(admin.StackedInline):  # Puoi usare anche StackedInline
#     model = GoalGeneration
#     max_num = 1
#
# class AgentAdmin(BaseAdmin):
#     list_display = ("name",)
#     search_fields = ("name",)
#     list_filter = ("name",)
#     inlines = [GoalGenerationInline]

# myapp/admin.py

from django.contrib import admin

@admin.register(Agent)
class MyModelAdmin(admin.ModelAdmin):
    form = MyModelForm


#admin.site.register(Agent, AgentAdmin)
