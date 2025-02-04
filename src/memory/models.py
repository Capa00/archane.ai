from django.db import models

from agents.abstract_module import AbstractModule


class LTM(AbstractModule):
    data = models.JSONField()


class STM(AbstractModule):
    data = models.JSONField()


class WM(AbstractModule):
    data = models.JSONField()