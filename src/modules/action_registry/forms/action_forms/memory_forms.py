from django import forms

from memories.models import Memory


class WriteMemoryConfigForm(forms.Form):
    memory = forms.ModelChoiceField(queryset=Memory.objects.all())

    def clean(self):
        cleaned_data = super().clean()
        cleaned_data['memory'] = cleaned_data['memory'].id
        return cleaned_data


class ReadMemoryConfigForm(WriteMemoryConfigForm):
    ...

class ReadMemoryInputForm(forms.Form):
    json_path = forms.CharField(max_length=255)