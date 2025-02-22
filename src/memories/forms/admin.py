from django import forms
from django.utils.translation import gettext_lazy as _
import importlib

from django_json_widget.widgets import JSONEditorWidget
from django_jsonform.forms.fields import JSONFormField
from django.contrib.admin.widgets import FilteredSelectMultiple

from memories.models import Memory
from modules.forms.fields.subform_field import SubFormField
from agents.models import Agent


class MemoryAdminForm(forms.ModelForm):
    agents = forms.ModelMultipleChoiceField(
        queryset=Agent.objects.all(),
        required=False,
        widget=FilteredSelectMultiple("Agents", is_stacked=False),
        label=_("Agents")
    )

    class Meta:
        model = Memory
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Recupera il valore di schema: da initial o dall'istanza
        schema = self.initial.get("schema") or (self.instance and self.instance.schema)

        if not schema:
            # Se schema è vuoto o None, il campo data usa JSONEditorWidget
            self.fields["data"] = forms.JSONField(
                widget=JSONEditorWidget,
                required=False,
                label=_("Data")
            )
        elif isinstance(schema, dict) and "form" in schema:
            # Se lo schema contiene un riferimento a un form custom, prova a importare la classe
            form_str = schema.get("form")
            try:
                module_path, form_class_name = form_str.rsplit(".", 1)
                mod = importlib.import_module(module_path)
                form_class = getattr(mod, form_class_name)
            except (ImportError, AttributeError) as e:
                # Se l'import fallisce, usa come fallback il JSONFormField con lo schema corrente
                self.fields["data"] = forms.JSONField(
                    widget=JSONEditorWidget,
                    required=False,
                    label=_("Data")
                )
            else:
                # Se l'import ha successo, usa il SubFormField con il form custom
                self.fields["data"] = SubFormField(
                    form_class,
                    label=_("Data"),
                    required=False
                )
        else:
            # Se schema non è vuoto ma non contiene "form", usa il JSONFormField
            self.fields["data"] = JSONFormField(
                schema=schema,
                label=_("Data"),
                required=False
            )
