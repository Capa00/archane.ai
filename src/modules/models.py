import logging
from importlib import import_module
from typing import Any, Dict

from django.db import models, transaction
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from modules.action_registry import get_action_choices, ACTION_REGISTRY

logger = logging.getLogger(__name__)


class Module(models.Model):
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
            default_schema = getattr(ACTION_REGISTRY[self.funcname], f"DEFAULT_{field_name.upper}_SCHEMA", False)
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
        return f"{self.name} - {self.funcname}"

    def execute(self, inputs: Dict[str, Any], config: Dict[str, Any]) -> Any:
        ...


class ModuleAction(models.Model):
    """
    Collega un modulo a una specifica azione (comando),
    permettendo di incapsulare il comando in un contesto specifico.
    """
    module: Module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name="module_actions")
    action: Action = models.ForeignKey(Action, on_delete=models.CASCADE, related_name="module_actions")
    config: dict = models.JSONField(_("Config"), default=dict, null=True, blank=True)

    order: int = models.PositiveIntegerField(
        default=0,
        help_text="Ordine di esecuzione del comando nel contesto del modulo"
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['module', 'action'], name='unique_module_action')
        ]
        ordering = ['order']

    def execute(self, inputs: Dict[str, Any], config: Dict[str, Any]) -> Any:
        """
        Esegue il comando incapsulato nell'azione.
        Qui potresti aggiungere logiche specifiche relative al contesto.
        """
        return self.action.execute(inputs, config)

    def __str__(self) -> str:
        return f"{self.module.name} - {self.action.name}"


class Execution(models.Model):
    """
    Registra l'esecuzione di un comando (ModuleAction).
    """
    module_action: ModuleAction = models.ForeignKey(ModuleAction, on_delete=models.SET_NULL, null=True, blank=True)
    # created_by = models.OneToOneField(User, null=True, blank=True)

    started_at: timezone.datetime = models.DateTimeField(null=True, blank=True)
    finished_at: timezone.datetime = models.DateTimeField(null=True, blank=True)

    inputs: dict = models.JSONField(_("Inputs"), null=True, blank=True)
    config: dict = models.JSONField(_("Config"), default=dict, null=True, blank=True)
    output: dict = models.JSONField(_("Output"), null=True, blank=True)

    def execute_command(self) -> None:
        """
        Esegue il comando associato alla ModuleAction,
        registrando gli orari di inizio e fine e salvando l'output.
        """
        if not self.module_action:
            raise ValueError("ModuleAction non definito per questa esecuzione.")

        with transaction.atomic():
            self.started_at = timezone.now()
            # Se inputs o config sono None, vengono sostituiti con dizionari vuoti
            self.output = self.module_action.execute(self.inputs or {}, self.config or {})
            self.finished_at = timezone.now()
            self.save()

    def __str__(self) -> str:
        if self.module_action:
            return f"Execution {self.id} - {self.module_action}"
        return f"Execution {self.id} - Senza ModuleAction"
