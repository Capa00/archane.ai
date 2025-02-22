from django.db import models

# Create your models here.
class Memory(models.Model):
    name = models.CharField(max_length=50)
    agents = models.ManyToManyField('agents.Agent', related_name="memories", blank=True)
    schema = models.JSONField(null=True, blank=True, default=dict)
    data = models.JSONField(null=True, blank=True, default=dict)
