from django import forms

from modules.forms.widgets.subform_widget import SubFormWidget


class SubFormField(forms.Field):
    def __init__(self, form_class, *args, **kwargs):
        self.form_class = form_class
        if 'widget' not in kwargs:
            kwargs['widget'] = SubFormWidget(form_class)
        super().__init__(*args, **kwargs)

    def clean(self, value):
        self.form_class(value['data']).clean()
        return value

    def to_python(self, value):
        if not value:
            return {}
        return value
