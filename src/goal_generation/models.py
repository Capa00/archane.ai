import json
import os

from django.template import Template, Context
from mdeditor.fields import MDTextField
from openai import OpenAI

from agents.abstract_module import Module
from utils.openai_messages import Message


class GoalGeneration(Module):
    system_prompt = MDTextField(null=True, blank=True)

    def __str__(self):
        return f"{self.name} - {self.agent.name}"

    def get_prompt_context(self):
        return Context({
            "data": json.dumps(self.data),
            "data_schema": json.dumps(self.data_schema),
            "output": json.dumps(self.output),
            "output_schema": json.dumps(self.output_schema),
            "agent": self.agent,
            "name": self.name,

        })

    def make_output(self, *args, **kwargs):
        template = Template(self.system_prompt)
        context = self.get_prompt_context()
        rendered_string = template.render(context)

        client = OpenAI(api_key=os.getenv("GOAL_GENERATION_APIKEY"), base_url="https://api.deepseek.com")
        message = Message(role=Message.Roles.SYSTEM, model='gpt-4o')
        message.add_text(rendered_string)

        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[message.get_message()],
            temperature=2,
        )
        response_string = response.choices[0].message.content

        self.output = json.loads(response_string)
