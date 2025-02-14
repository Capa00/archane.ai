from django import forms
from django_jsonform.forms.fields import JSONFormField
from mdeditor.fields import MDTextFormField

from modules.action_registry import register_action, ActionFunction


@register_action("llm_openai_like")
class LLMOpenAILikeAction(ActionFunction):
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

    def get_config_form(self):
        return LLMOpenAILikeActionConfigForm

    def get_input_form(self):
        return LLMOpenAILikeActionInputForm

    def __call__(self, inputs, config):

        return {"output": " ".join(inputs['input'])}


class LLMOpenAILikeActionInputForm(forms.Form):
    prompt_context = forms.CharField(widget=forms.Textarea, required=False)

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
    system_prompt = MDTextFormField(required=False)
    data = JSONFormField(schema=DATA_SCHEMA, required=False)
