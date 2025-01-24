from django.contrib import admin
from django import forms
from django_json_widget.widgets import JSONEditorWidget
from .models import TargetAudience

class TargetAudienceForm(forms.ModelForm):
    class Meta:
        model = TargetAudience
        fields = '__all__'
        widgets = {
            'age_range': JSONEditorWidget(),  # Usa il widget JSON per il campo age_range
        }

@admin.register(TargetAudience)
class TargetAudienceAdmin(admin.ModelAdmin):
    form = TargetAudienceForm