import logging
from typing import Any, Dict

import jsonschema
from django.db import models, transaction
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from modules.action_registry import get_action_choices, ACTION_REGISTRY

logger = logging.getLogger(__name__)


class Module(models.Model):
    agents = models.ManyToManyField('agents.Agent', related_name="modules", blank=True)
    name: str = models.CharField(_("Module Name"), max_length=255, unique=True)
    description: str = models.TextField(_("Description"), blank=True, null=True)
    created_at: timezone.datetime = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.name


class Action(models.Model):
    funcname: str = models.CharField(_("Function Name"),  choices=get_action_choices(), max_length=50)
    name: str = models.CharField(_("Name"), max_length=50)
    description: str = models.TextField(_("Description"), null=True, blank=True)

    input_schema: dict = models.JSONField(_("Input Schema"), null=True, blank=True)
    output_schema: dict = models.JSONField(_("Output Schema"), null=True, blank=True)
    config_schema: dict = models.JSONField(_("Config Schema"), null=True, blank=True)

    created_at: timezone.datetime = models.DateTimeField(auto_now_add=True)

    def _update_schema_if_none(self, field_name):
        if not getattr(self, field_name):
            default_schema = getattr(ACTION_REGISTRY[self.funcname], field_name.upper(), False)
            if default_schema:
                setattr(self, field_name, default_schema)

    def save(self, *args, **kwargs):
        self._update_schema_if_none('input_schema')
        self._update_schema_if_none('output_schema')
        self._update_schema_if_none('config_schema')

        return super().save(*args, **kwargs)

    class Meta:
        unique_together = ("funcname", "name")

    def __str__(self):
        return f"{self.name} ({self.funcname})"

    def execute(self, inputs: Dict[str, Any], config: Dict[str, Any]) -> Any:
        jsonschema.validate(instance=inputs, schema=self.input_schema)
        jsonschema.validate(instance=config, schema=self.config_schema)
        return ACTION_REGISTRY[self.funcname]()(inputs, config)


class ModuleAction(models.Model):
    module: Module = models.ForeignKey(Module, on_delete=models.SET_NULL, related_name="module_actions", null=True)
    action: Action = models.ForeignKey(Action, on_delete=models.SET_NULL, related_name="module_actions", null=True)
    configs: dict = models.JSONField(_("Config"), default=dict, null=True, blank=True)
    inputs: dict = models.JSONField(_("Input"), default=dict, null=True, blank=True)

    def execute_action(self, inputs: Dict[str, Any], config: Dict[str, Any]) -> Any:
        return self.action.execute(inputs, config)

    def execute(self, inputs, config, user=None) -> Any:
        with transaction.atomic():
            self.inputs = inputs
            self.config = config
            self.save()

            execution = Execution(
                module_action=self,
                inputs=self.inputs,
                configs=self.configs,
            )

            execution.set_created_by(user)
            execution.started_at = timezone.now()
            execution.save()

            execution.output = self.execute_action(self.inputs, self.configs)
            execution.finished_at = timezone.now()
            execution.save()

            return execution

    def __str__(self) -> str:
        return f"{self.module} / {self.action}"


class Execution(models.Model):
    """
    Registra l'esecuzione di un comando (ModuleAction).
    """
    module_action: ModuleAction = models.ForeignKey(ModuleAction, on_delete=models.SET_NULL, null=True, blank=True)
    # created_by = models.OneToOneField(User, null=True, blank=True)

    started_at: timezone.datetime = models.DateTimeField(null=True, blank=True)
    finished_at: timezone.datetime = models.DateTimeField(null=True, blank=True)

    inputs: dict = models.JSONField(_("Inputs"), null=True, blank=True)
    configs: dict = models.JSONField(_("Config"), default=dict, null=True, blank=True)
    output: dict = models.JSONField(_("Output"), null=True, blank=True)

    def set_created_by(self, user):
        self.created_by = user



    def __str__(self) -> str:
        if self.module_action:
            return f"Execution {self.id} - {self.module_action}"
        return f"Execution {self.id} - Senza ModuleAction"
