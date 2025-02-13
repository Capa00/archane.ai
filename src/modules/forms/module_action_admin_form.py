from django_jsonform.widgets import JSONFormWidget
from django import forms

from modules.models import ModuleAction


class ModuleActionForm(forms.ModelForm):
    class Meta:
        model = ModuleAction
        fields = '__all__'
        widgets = {
            'config': JSONFormWidget(schema={}),
            'input': JSONFormWidget(schema={}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Se è presente l'istanza e l'azione associata, utilizza lo schema definito in Action.config_schema
        if self.instance and getattr(self.instance, 'action', None):
            self.fields['configs'].widget = JSONFormWidget(schema=self.instance.action.config_schema or {})
            self.fields['inputs'].widget = JSONFormWidget(schema=self.instance.action.input_schema or {})
        else:
            self.fields['configs'].widget = JSONFormWidget(schema={})
            self.fields['inputs'].widget = JSONFormWidget(schema={})