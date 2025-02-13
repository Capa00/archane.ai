import importlib
import pkgutil
import os

from django import forms
from django_jsonform.forms.fields import JSONFormField

ACTION_REGISTRY = {}

def register_action(name):
    """Decorator per registrare un'azione nella registry"""

    def wrapper(func):
        if name in ACTION_REGISTRY:
            raise ValueError(f"L'azione '{name}' è già registrata.")

        ACTION_REGISTRY[name] = func
        return func

    return wrapper


def get_action_function(funcname):
    return ACTION_REGISTRY[funcname]


def get_action_choices():
    """Restituisce le azioni registrate come scelte per Django Admin"""
    return sorted([(key, key.replace("_", " ").capitalize()) for key in ACTION_REGISTRY.keys()])


class ActionFunction:
    INPUT_SCHEMA = {}
    OUTPUT_SCHEMA = {}
    CONFIG_SCHEMA = {}

    # def get_input_form(self, *args, **kwargs):
    #     return ActionFunctionForm()
    #
    # def get_output_form(self, *args, **kwargs):
    #     return ActionFunctionForm()
    #
    def get_config_form(self, *args, **kwargs):
        class ActionConfigForm(forms.Form):
            configs = JSONFormField(schema=self.CONFIG_SCHEMA)
        return ActionConfigForm


package_name = __name__
package_path = os.path.dirname(__file__)
# Scansiona tutti i moduli nel package e importali dinamicamente
for _, module_name, _ in pkgutil.iter_modules([package_path]):
    importlib.import_module(f"{package_name}.{module_name}")