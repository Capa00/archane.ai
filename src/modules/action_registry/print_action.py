from django import forms
from django_jsonform.forms.fields import JSONFormField
from mdeditor.fields import MDTextFormField

from modules.action_registry import register_action, ActionFunction


@register_action("print")
class PrintAction(ActionFunction):
    INPUT_SCHEMA = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "type": "array",
        "items": {
            "type": "string"
        }
    }

    OUTPUT_SCHEMA = {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "type": "object",
        "properties": {
            "output": {
                "type": "string",
                "description": "Una stringa"
            }
        },
        "required": ["output"],
        "additionalProperties": False,
    }

    CONFIG_SCHEMA = {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "type": "object",
        "properties": {
            "output": {
                "type": "string",
                "description": "Una stringa"
            }
        },
        "required": ["output"],
        "additionalProperties": False,
    }


    def __call__(self, inputs, config):
        return {"output": " ".join(inputs['input'])}


class PrintActionConfigForm(forms.Form):
    prompt = MDTextFormField()
    other_data = JSONFormField(schema=PrintAction.CONFIG_SCHEMA)

    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data