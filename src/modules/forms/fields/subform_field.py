from django import forms
from modules.forms.widgets.subform_widget import SubFormWidget

class SubFormField(forms.Field):
    def __init__(self, form_class, *args, **kwargs):
        if 'widget' not in kwargs:
            kwargs['widget'] = SubFormWidget(form_class)

        super().__init__(*args, **kwargs)
        self.form_class = form_class
        self.subform = None

    def clean(self, value):
        # Istanzia il subform con i dati ricevuti e verifica la validità
        self.subform = self.widget.form_class(value)
        if not self.subform.is_valid():
            raise forms.ValidationError(self.subform.errors)
        return self.subform.cleaned_data
