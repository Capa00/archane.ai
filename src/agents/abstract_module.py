from django.db import models
from django_jsonform.models.fields import JSONField


class Module(models.Model):
    name = models.CharField(max_length=50)
    agent = models.ForeignKey("agents.Agent", on_delete=models.SET_NULL, null=True, related_name="modules")

    data_schema = models.JSONField(null=True, blank=True, default=dict)
    data = JSONField(null=True, blank=True)

    output_schema = models.JSONField(null=True, blank=True, default=dict)
    output = JSONField(null=True, blank=True)

    def get_data_schema(self):
        return self.data_schema or {"type": "object", "properties": {}}

    def get_output_schema(self):
        return self.output_schema or {"type": "object", "properties": {}}