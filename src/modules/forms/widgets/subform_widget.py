from django import forms
from django.template.loader import render_to_string


class SubFormWidget(forms.Widget):
    template_name = "modules/widgets/subform_widget.html"

    def __init__(self, form_class, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.form_class = form_class

    def render(self, name, value, attrs=None, renderer=None):
        if value is None:
            value = {}
        form = self.form_class(initial=value)
        return render_to_string(self.template_name, {"form": form})

    def value_from_datadict(self, data, files, name):
        prefix = f"{name}-subform"
        form = self.form_class(data=data, files=files)

        if form.is_bound and form.is_valid():
            return form.cleaned_data
        else:
            return data

    @property
    def media(self):
        combined = forms.Media()
        if self.form_class:
            dummy_form = self.form_class()
            for field_name in dummy_form.fields:
                combined += dummy_form[field_name].field.widget.media
        return combined
