from django.db import models
from mdeditor.fields import MDTextField


class AbstractModule(models.Model):
    name = models.CharField(max_length=50)
    system_prompt = MDTextField(null=True, blank=True)
    agent = models.ForeignKey("agents.Agent", on_delete=models.SET_NULL, null=True)

    class Meta:
        abstract = True