from django.contrib import admin
from django import forms

from agents.models import Agent
from modules.models import Module


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