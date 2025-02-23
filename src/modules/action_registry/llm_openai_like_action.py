import os

from django import forms
from django.template import Template, Context
from django_jsonform.forms.fields import JSONFormField
from mdeditor.fields import MDTextFormField
from openai import OpenAI

from modules.action_registry import register_action, ActionFunction
from utils.openai_messages import ChatMessage


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

    def __call__(self, module_action, inputs, config):
        api_key = config.get('api_key') or os.environ.get("OPENAI_API_KEY")
        if config['base_url']:
            client = OpenAI(base_url=config['base_url'], api_key=api_key)
        else:
            client = OpenAI(api_key=api_key)
        prompt_context = inputs['prompt_context']
        template = config['system_prompt']

        template_obj = Template(template)
        context_obj = Context(prompt_context)
        system_prompt = template_obj.render(context_obj)
        system_prompt_message = ChatMessage(role=ChatMessage.Roles.SYSTEM)
        system_prompt_message.add_text(system_prompt)
        response = client.chat.completions.create(**config['data'], messages=[system_prompt_message.get_message()])
        return {"response": response.choices[0].message.content}
