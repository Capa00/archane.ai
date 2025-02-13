from django.forms import HiddenInput
from django_jsonform.widgets import JSONFormWidget
from django import forms

from modules.action_registry import get_action_function
from modules.forms.action_function_form import ActionFunctionForm
from modules.forms.fields.subform_field import SubFormField
from modules.forms.widgets.subform_widget import SubFormWidget
from modules.models import ModuleAction


class ModuleActionForm(forms.ModelForm):
    configs = SubFormField(form_class=ActionFunctionForm)

    class Meta:
        model = ModuleAction
        fields = '__all__'
        widgets = {
    #        'config': JSONFormWidget(schema={}),
            #'input': JSONFormWidget(schema={}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and getattr(self.instance, 'action', None):
            #self.fields['inputs'].widget = JSONFormWidget(schema=self.instance.action.input_schema or {})
            action_function = get_action_function(self.instance.action.funcname)
            self.fields['configs'].widget = SubFormWidget(action_function().get_config_form())
        # else:
        #      #self.fields['configs'].widget = JSONFormWidget(schema={})
        #      self.fields['inputs'].widget = JSONFormWidget(schema={})

    def clean(self):
        s = super().clean()
        return s