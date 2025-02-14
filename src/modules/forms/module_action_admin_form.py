from django import forms
from modules.action_registry import get_action_function
from modules.forms.fields.subform_field import SubFormField
from modules.forms.widgets.subform_widget import SubFormWidget
from modules.models import ModuleAction

class ModuleActionForm(forms.ModelForm):
    configs = SubFormField(form_class=forms.Form)
    inputs = SubFormField(form_class=forms.Form)

    class Meta:
        model = ModuleAction
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        default_widget = SubFormWidget(forms.Form)
        self.fields['configs'].widget = default_widget
        self.fields['inputs'].widget = default_widget

        if not (self.instance and getattr(self.instance, 'action', None)):
            return

        action_function = get_action_function(self.instance.action.funcname)
        if not action_function:
            return

        action_instance = action_function()
        self.fields['configs'] = SubFormField(form_class=action_instance.get_config_form())
        self.fields['inputs'] = SubFormField(form_class=action_instance.get_input_form())
