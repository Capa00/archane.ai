# subform_widget.py
from django import forms
from django.template.loader import render_to_string

class SubFormWidget(forms.Widget):
    template_name = "modules/widgets/subform_widget.html"

    def __init__(self, form_class, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.form_class = form_class
        self.subform = None

    def render(self, name, value, attrs=None, renderer=None):
        # Imposta un prefisso per il subform
        prefix = f"{name}-subform"
        if value is None:
            value = {}
        form = self.form_class(initial=value, prefix=prefix)
        return render_to_string(self.template_name, {"form": form, "name": name})

    def value_from_datadict(self, data, files, name):
        prefix = f"{name}-subform"
        self.subform = self.form_class(data=data, files=files, prefix=prefix)
        if self.subform.is_bound:
            if self.subform.is_valid():
                return self.subform.cleaned_data
            else:
                raise forms.ValidationError(self.subform.errors)
        return {}

    @property
    def media(self):
        combined = forms.Media()
        if self.form_class:
            dummy_form = self.form_class(prefix="dummy")
            for field_name in dummy_form.fields:
                combined += dummy_form[field_name].field.widget.media
        return combined
