import importlib
import pkgutil
import os
from abc import ABC, abstractmethod


ENVOBSERVER_REGISTRY = {}

def register_observer(name):
    """Decorator per registrare un'azione nella registry"""

    def wrapper(func):
        if name in ENVOBSERVER_REGISTRY:
            raise ValueError(f"L'observer '{name}' è già registrato.")

        ENVOBSERVER_REGISTRY[name] = func
        return func

    return wrapper


def get_observer_function(funcname):
    return ENVOBSERVER_REGISTRY[funcname]


def get_observer_choices():
    return sorted([(key, key.replace("_", " ").capitalize()) for key in ENVOBSERVER_REGISTRY.keys()])


class Observer(ABC):
    CONFIG_SCHEMA = {}

    @abstractmethod
    def observe(self):
        ...



package_name = __name__
package_path = os.path.dirname(__file__)
# Scansiona tutti i moduli nel package e importali dinamicamente
for _, module_name, _ in pkgutil.iter_modules([package_path]):
    importlib.import_module(f"{package_name}.{module_name}")