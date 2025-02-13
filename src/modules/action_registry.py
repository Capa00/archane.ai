ACTION_REGISTRY = {}


def register_action(name):
    """Decorator per registrare un'azione nella registry"""

    def wrapper(func):
        if name in ACTION_REGISTRY:
            raise ValueError(f"L'azione '{name}' è già registrata.")

        ACTION_REGISTRY[name] = func
        return func

    return wrapper


def get_action_choices():
    """Restituisce le azioni registrate come scelte per Django Admin"""
    return sorted([(key, key.replace("_", " ").capitalize()) for key in ACTION_REGISTRY.keys()])


@register_action("chat openai like")
class ChatOpenAILikeAction:
    def __call__(self, inputs, config):
        pass


@register_action("tanti saluti")
class HelloWorldAction:
    def __call__(self, inputs, config):
        pass


@register_action("print")
class PrintAction:
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
        "type": "string"
    }

    def __call__(self, inputs, config):
            return {"output": " ".join(inputs['input'])}
