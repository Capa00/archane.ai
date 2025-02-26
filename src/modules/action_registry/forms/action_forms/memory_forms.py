from django import forms
from django_json_widget.widgets import JSONEditorWidget

from memories.models import Memory


class MemoryFormBase(forms.Form):
    memory = forms.ModelChoiceField(queryset=Memory.objects.all(), required=False)

    def clean(self):
        cleaned_data = super().clean()
        memory = cleaned_data.get("memory")
        if memory:
            cleaned_data['memory'] = memory.id
        return cleaned_data


class WriteMemoryConfigForm(MemoryFormBase):
    data = forms.JSONField(widget=JSONEditorWidget, required=False)

class ReadMemoryConfigForm(MemoryFormBase):
    json_path = forms.CharField(max_length=255, required=False)
