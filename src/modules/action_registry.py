ACTION_REGISTRY = {}

def register_action(name):
    """Decorator per registrare un'azione nella registry"""
    def wrapper(func):
        ACTION_REGISTRY[name] = func
        return func
    return wrapper

def get_action_choices():
    """Restituisce le azioni registrate come scelte per Django Admin"""
    return [(key, key.capitalize()) for key in ACTION_REGISTRY.keys()]


@register_action("chat openai like")
def chat_openai_like_action(inputs, config):
    ...

@register_action("tanti saluti")
def chat_openai_like_action(inputs, config):
    ...

@register_action("print")
def print_action(inputs, config):
    print(inputs)
