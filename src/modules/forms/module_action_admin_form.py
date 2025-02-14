from django import forms
from modules.action_registry import get_action_function
from modules.forms.fields.subform_field import SubFormField
from modules.forms.widgets.subform_widget import SubFormWidget
from modules.models import ModuleAction

class ModuleActionForm(forms.ModelForm):
    configs = SubFormField(form_class=forms.Form)

    class Meta:
        model = ModuleAction
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and getattr(self.instance, 'action', None):
            try:
                action_function = get_action_function(self.instance.action.funcname)
                action_instance = action_function() if action_function else None
                if action_instance and hasattr(action_instance, 'get_config_form'):
                    config_form_class = action_instance.get_config_form()
                    self.fields['configs'] = SubFormField(form_class=config_form_class)
                    #self.fields['configs'].widget = SubFormWidget(config_form_class)
                else:
                    self.fields['configs'].widget = SubFormWidget(forms.Form)
            except Exception as e:
                self.fields['configs'].widget = SubFormWidget(forms.Form)
        else:
            self.fields['configs'].widget = SubFormWidget(forms.Form)
