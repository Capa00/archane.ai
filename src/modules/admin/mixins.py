import importlib

from django import forms
from django.db.models import JSONField
from django_json_widget.widgets import JSONEditorWidget
from django.utils.translation import gettext_lazy as _
from django_jsonform.forms.fields import JSONFormField

from modules.forms.fields.subform_field import SubFormField

def get_nested_attr(instance, attr_path):
    for attr in attr_path.split('.'):
        instance = getattr(instance, attr, None)
        if instance is None:
            return None
    return instance


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
            # Imposta il widget per il campo schema
            if schema_field in self.fields:
                self.fields[schema_field].widget = JSONEditorWidget()

            # Recupera lo schema: supporta anche notazione annidata (es. "action.input_schema")
            if '.' in schema_field:
                schema_value = self.initial.get(schema_field) or (
                            self.instance and get_nested_attr(self.instance, schema_field))
            else:
                schema_value = self.initial.get(schema_field) or (
                            self.instance and getattr(self.instance, schema_field)) or None

            # Procedi come nel codice originale per configurare il campo data in base allo schema
            if not schema_value:
                self.fields[data_field] = forms.JSONField(
                    widget=JSONEditorWidget(),
                    required=False,
                    label=self.fields.get(data_field, {}).label or _(data_field.capitalize())
                )
            elif isinstance(schema_value, dict) and "form" in schema_value:
                form_str = schema_value.get("form")
                try:
                    module_path, form_class_name = form_str.rsplit(".", 1)
                    mod = importlib.import_module(module_path)
                    form_class = getattr(mod, form_class_name)
                except (ImportError, AttributeError):
                    self.fields[data_field] = forms.JSONField(
                        widget=JSONEditorWidget,
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


class ExternalSchemaBasedFormMixin:
    # Questo dizionario deve essere impostato dalla classe admin, es:
    # external_schemas_mapping = {"action.input_schema": "inputs"}
    external_schemas_mapping = {}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Per ogni mapping, otteniamo lo schema dall'istanza esterna
        for external_schema_field, data_field in self.external_schemas_mapping.items():
            # Supponiamo che la stringa sia del tipo "relation_field.schema_field"
            parts = external_schema_field.split('.')
            if len(parts) == 2 and self.instance:
                relation_field, schema_field = parts
                related_instance = getattr(self.instance, relation_field, None)
                schema_value = related_instance and getattr(related_instance, schema_field, None)
            else:
                schema_value = None

            # Configuriamo il campo dati (ad es. "inputs") in base allo schema esterno
            if not schema_value:
                # Se non è definito uno schema esterno, usiamo un campo JSON semplice
                self.fields[data_field] = forms.JSONField(
                    widget=JSONEditorWidget(),
                    required=False,
                    label=self.fields.get(data_field, {}).label or _(data_field.capitalize())
                )
            elif isinstance(schema_value, dict) and "form" in schema_value:
                # Se lo schema contiene una chiave "form", proviamo a importare il form specificato
                form_str = schema_value.get("form")
                try:
                    module_path, form_class_name = form_str.rsplit(".", 1)
                    mod = importlib.import_module(module_path)
                    form_class = getattr(mod, form_class_name)
                except (ImportError, AttributeError):
                    # Fallback: usiamo un JSONField con schema
                    self.fields[data_field] = forms.JSONField(
                        widget=JSONEditorWidget(),
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
                # Altrimenti, usiamo un JSONFormField che usa lo schema per validare il dato
                self.fields[data_field] = JSONFormField(
                    schema=schema_value,
                    label=self.fields.get(data_field, {}).label or _(data_field.capitalize()),
                    required=False
                )


class ExternalSchemaBasedAdminMixin:
    # Il mapping viene definito qui, per esempio:
    # external_schemas_mapping = {"action.input_schema": "inputs"}
    external_schemas_mapping = {}

    def get_form(self, request, obj=None, **kwargs):
        base_form_class = super().get_form(request, obj, **kwargs)
        # Creiamo una nuova classe form che eredita dal mixin e dal form base
        class ExternalSchemaBasedForm(ExternalSchemaBasedFormMixin, base_form_class):
            pass
        ExternalSchemaBasedForm.external_schemas_mapping = self.external_schemas_mapping
        return ExternalSchemaBasedForm


class ExternalSchemaBasedInlineAdminMixin:
    external_schemas_mapping = {}

    def get_formset(self, request, obj=None, **kwargs):
        formset = super().get_formset(request, obj, **kwargs)
        OriginalForm = formset.form

        class InlineForm(ExternalSchemaBasedFormMixin, OriginalForm):
            pass

        InlineForm.external_schemas_mapping = self.external_schemas_mapping
        formset.form = InlineForm
        return formset


class SchemaBasedInlineAdminMixin:
    schemas_mapping = {}

    def get_formset(self, request, obj=None, **kwargs):
        formset = super().get_formset(request, obj, **kwargs)
        OriginalForm = formset.form

        class InlineForm(SchemaBasedFormMixin, OriginalForm):
            pass

        InlineForm.schemas_mapping = self.schemas_mapping
        formset.form = InlineForm
        return formset

