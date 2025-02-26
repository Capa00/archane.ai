import json

from django.template import Template, Context
from jsonpath_ng import parse

from memories.models import Memory
from modules.action_registry import register_action, ActionFunction


@register_action("read_memory")
class ReadMemoryAction(ActionFunction):
    def __call__(self, module_action, inputs, config):
        memory = Memory.objects.get(id=config['memory'])
        if config:
            jsonpath_expr = parse(config['json_path'])
            matches = jsonpath_expr.find(memory.data)
            if matches:
                res = [match.value for match in matches]
                return res if len(res) > 1 else res[0]



@register_action("write_memory")
class WriteMemoryAction(ActionFunction):
    def __call__(self, module_action, inputs, config):
        memory = Memory.objects.get(id=config['memory'])
        data = config['data']
        if data:
            data_template = Template(json.dumps(data))
            data_context = Context(inputs)
            data_dict = json.loads(data_template.render(data_context))
            memory.data.update(**data_dict)
            memory.save()
