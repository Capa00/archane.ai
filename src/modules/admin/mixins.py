import importlib

from django import forms
from django.db.models import JSONField
from django_json_widget.widgets import JSONEditorWidget
from django.utils.translation import gettext_lazy as _
from django_jsonform.forms.fields import JSONFormField

from modules.forms.fields.subform_field import SubFormField


class JSONWidgetAdminMixin:
    formfield_overrides = {
        JSONField: {'widget': JSONEditorWidget},
    }


class SchemaBasedFormMixin:
    # Questo dizionario deve essere impostato dal mixin admin (es. {"schema1": "input", "output_schema": "output"})
    schemas_mapping = {}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Per ogni coppia schema_field -> data_field, configuriamo i campi
        for schema_field, data_field in self.schemas_mapping.items():
            # Imposta sempre il widget JSONEditorWidget per il campo schema
            if schema_field in self.fields:
                self.fields[schema_field].widget = JSONEditorWidget()
            # Recupera il valore dello schema: dai dati iniziali o dall'istanza
            schema_value = self.initial.get(schema_field) or (
                    self.instance and getattr(self.instance, schema_field)
            ) or None

            if not schema_value:
                # Se lo schema è vuoto o None, il campo data usa un JSONField con JSONEditorWidget
                self.fields[data_field] = forms.JSONField(
                    widget=JSONEditorWidget(),
                    required=False,
                    label=self.fields.get(data_field, {}).label or _(data_field.capitalize())
                )
            elif isinstance(schema_value, dict) and "form" in schema_value:
                # Se lo schema contiene "form", tenta di importare dinamicamente il form indicato
                form_str = schema_value.get("form")
                try:
                    module_path, form_class_name = form_str.rsplit(".", 1)
                    mod = importlib.import_module(module_path)
                    form_class = getattr(mod, form_class_name)
                except (ImportError, AttributeError):
                    # Fallback: usa il JSONFormField con lo schema corrente
                    self.fields[data_field] = forms.JSONField(
                        widget=JSONEditorWidget,
                        schema=schema_value,
                        label=self.fields.get(data_field, {}).label or _(data_field.capitalize()),
                        required=False
                    )
                else:
                    self.fields[data_field] = SubFormField(
                        form_class,
                        label=self.fields.get(data_field, {}).label or _(data_field.capitalize()),
                        required=False
                    )
            else:
                # Altrimenti, usa il JSONFormField con lo schema fornito
                self.fields[data_field] = JSONFormField(
                    schema=schema_value,
                    label=self.fields.get(data_field, {}).label or _(data_field.capitalize()),
                    required=False
                )


class SchemaBasedAdminMixin:
    # Il mapping tra campi schema e campi dati deve essere definito nell'admin
    schemas_mapping = {}

    def get_form(self, request, obj=None, **kwargs):
        base_form_class = super().get_form(request, obj, **kwargs)
        # Crea una nuova classe form che eredita dal mixin e dal form base
        class SchemaBasedForm(SchemaBasedFormMixin, base_form_class):
            pass
        SchemaBasedForm.schemas_mapping = self.schemas_mapping
        return SchemaBasedForm

    def get_fieldsets(self, request, obj=None):
        # Se l'admin non ha definito fieldsets esplicitamente, creiamo una suddivisione automatica:
        all_fields = self.get_fields(request, obj)
        # Costruiamo la lista dei campi legati agli schema
        schema_fields = []
        for schema_field, data_field in self.schemas_mapping.items():
            schema_fields.append(schema_field)
        # Rimuovo eventuali duplicati
        schema_fields = list(dict.fromkeys(schema_fields))
        # I restanti campi vengono messi nel fieldset principale
        main_fields = [f for f in all_fields if f not in schema_fields]

        fieldsets = []
        if main_fields:
            fieldsets.append((_('Main Information'), {'fields': main_fields}))
        if schema_fields:
            fieldsets.append((_('Schemas'), {'classes': ('collapse',), 'fields': schema_fields}))
        return fieldsets