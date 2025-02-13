from django import forms
from django.contrib import admin

from agents.models import Agent
from modules.models import Module


class AgentAdminForm(forms.ModelForm):
    modules = forms.ModelMultipleChoiceField(
        queryset=Module.objects.all(),
        widget=admin.widgets.FilteredSelectMultiple("Modules", is_stacked=False),
        required=False
    )

    class Meta:
        model = Agent
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['modules'].initial = self.instance.modules.all()

    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            instance.save()
        if instance.pk:
            instance.modules.set(self.cleaned_data['modules'])  # Aggiorna i moduli associati
        return instance

class ModuleInline(admin.StackedInline):
    model = Module.agents.through
    extra = 0

class AgentAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)
    list_filter = ("name",)

    form = AgentAdminForm
    inlines = [ModuleInline]

admin.site.register(Agent, AgentAdmin)
