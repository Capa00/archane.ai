from django import forms
from django_jsonform.forms.fields import JSONFormField
from mdeditor.fields import MDTextFormField

from modules.action_registry import register_action, ActionFunction


@register_action("llm_openai_like")
class LLMOpenAILikeAction(ActionFunction):
    INPUT_SCHEMA = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "type": "object",
        "properties": {
            "system_prompt": {
                "type": "string"
            },
            "data": {
                "type": "array",
                "items": {
                    "type": "string"
                }
            }
        },
        "required": ["system_prompt", "data"],
        "additionalProperties": False
    }

    OUTPUT_SCHEMA = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "type": "object",
        "properties": {
            "output": {
                "type": "string"
            },
            "token": {
                "type": "integer"
            }
        },
        "required": ["output", "token"]
    }

    CONFIG_SCHEMA = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "type": "object",
        "properties": {
            "system_prompt": {
                "type": "string"
            },
            "data": {
                "type": "array",
                "items": {
                    "type": "string"
                }
            }
        },
        "required": ["system_prompt", "data"],
        "additionalProperties": False
    }

    def get_config_form(self):
        return LLMOpenAILikeActionConfigForm

    def __call__(self, inputs, config):
        return {"output": " ".join(inputs['input'])}


class LLMOpenAILikeActionConfigForm(forms.Form):
    DATA_SCHEMA = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "type": "object",
        "properties": {
            "data": {
                "type": "array",
                "items": {
                    "type": "string"
                }
            }
        },
        "required": ["data"],
        "additionalProperties": False
    }
    prompt = MDTextFormField()
    data = JSONFormField(schema=DATA_SCHEMA)

    def is_valid(self):
        return super().is_valid()

    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data
