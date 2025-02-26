import logging
from typing import Any, Dict

from django.db import models, transaction
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model

from modules.action_registry import get_action_choices, ACTION_REGISTRY

User = get_user_model()
logger = logging.getLogger(__name__)


class Module(models.Model):
    name: str = models.CharField(_("Module Name"), max_length=255, unique=True)
    description: str = models.TextField(_("Description"), blank=True, null=True)
    created_at: timezone.datetime = models.DateTimeField(auto_now_add=True)
    agents = models.ManyToManyField('agents.Agent', related_name="modules", blank=True)

    def duplicate(self) -> "Module":
        with transaction.atomic():
            base_name = f"{self.name} (copy)"
            new_name = base_name
            counter = 1
            while Module.objects.filter(name=new_name).exists():
                new_name = f"{base_name} {counter}"
                counter += 1

            dup_module = Module.objects.create(
                name=new_name,
                description=self.description,
            )
            dup_module.agents.set(self.agents.all())
            for mod_action in self.module_actions.all():
                mod_action.duplicate(new_module=dup_module)
            return dup_module

    def execute(self, inputs: Dict[str, Any] = None, user: User = None):
        outputs = []
        with transaction.atomic():
            for module_action in self.module_actions.all():
                execution = module_action.execute(inputs, user)
                outputs.append(execution.output)
                inputs = {"input": execution.output, "outputs": outputs}

    def __str__(self) -> str:
        return self.name


class Action(models.Model):
    funcname: str = models.CharField(
        _("Function Name"),
        choices=get_action_choices(),
        max_length=50
    )
    name: str = models.CharField(_("Name"), max_length=50)
    description: str = models.TextField(_("Description"), null=True, blank=True)

    input_schema: dict = models.JSONField(_("Input Schema"), null=True, blank=True)
    output_schema: dict = models.JSONField(_("Output Schema"), null=True, blank=True)
    config_schema: dict = models.JSONField(_("Config Schema"), null=True, blank=True)

    created_at: timezone.datetime = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("funcname", "name")

    # def _update_schema_if_none(self, field_name: str) -> None:
    #     current_value = getattr(self, field_name)
    #     if current_value is None:
    #         default_schema = getattr(ACTION_REGISTRY.get(self.funcname, object()), field_name.upper(), None)
    #         if default_schema is not None:
    #             setattr(self, field_name, default_schema)
    #
    # def save(self, *args, **kwargs):
    #     # self._update_schema_if_none('input_schema')
    #     # self._update_schema_if_none('output_schema')
    #     # self._update_schema_if_none('config_schema')
    #     return super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({self.funcname})"

    def execute(self, module_action: "ModuleAction", inputs: Dict[str, Any], configs: Dict[str, Any]) -> Any:
        try:
            action_callable = ACTION_REGISTRY[self.funcname]
        except KeyError:
            msg = f"Azione '{self.funcname}' non trovata in ACTION_REGISTRY."
            logger.error(msg)
            raise ValueError(msg)
        return action_callable()(module_action, inputs, configs)


class ModuleAction(models.Model):
    module: Module = models.ForeignKey(Module, on_delete=models.SET_NULL, related_name="module_actions", null=True)
    action: Action = models.ForeignKey(Action, on_delete=models.SET_NULL, related_name="module_actions", null=True)
    inputs: dict = models.JSONField(_("Input"), default=dict, null=True, blank=True)
    configs: dict = models.JSONField(_("Config"), default=dict, null=True, blank=True)

    class Meta:
        ordering = ['id']

    def execute_action(self, inputs: Dict[str, Any], configs: Dict[str, Any]) -> Any:
        return self.action.execute(self, inputs, configs)

    def execute(self, inputs: Dict[str, Any], user: User = None) -> "Execution":
        with transaction.atomic():
            self.inputs = inputs
            self.save()

            execution = Execution(
                module_action=self,
                inputs=self.inputs,
                configs=self.configs,
            )
            execution.set_created_by(user)
            execution.started_at = timezone.now()
            execution.save()

            try:
                execution.output = self.execute_action(self.inputs, self.configs)
            except Exception as e:
                logger.exception("Errore durante l'esecuzione dell'azione.")
                raise e
            execution.finished_at = timezone.now()
            execution.save()

            return execution

    def duplicate(self, new_module: Module = None) -> "ModuleAction":
        with transaction.atomic():
            dup = ModuleAction.objects.create(
                module=new_module if new_module is not None else self.module,
                action=self.action,
                configs=self.configs,
                inputs=self.inputs,
            )
            return dup

    def __str__(self) -> str:
        return f"{self.module} / {self.action}"


class Execution(models.Model):
    module_action: ModuleAction = models.ForeignKey(ModuleAction, on_delete=models.SET_NULL, null=True, blank=True)
    # created_by: User = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    started_at: timezone.datetime = models.DateTimeField(null=True, blank=True)
    finished_at: timezone.datetime = models.DateTimeField(null=True, blank=True)

    output: dict = models.JSONField(_("Output"), null=True, blank=True)
    inputs: dict = models.JSONField(_("Inputs"), null=True, blank=True)
    configs: dict = models.JSONField(_("Config"), default=dict, null=True, blank=True)

    def set_created_by(self, user: User) -> None:
        if user:
            self.created_by = user

    def __str__(self) -> str:
        if self.module_action:
            return f"Execution {self.id} - {self.module_action}"
        return f"Execution {self.id} - Senza ModuleAction"
