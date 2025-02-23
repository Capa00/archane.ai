from django.db import models

# Create your models here.
class Memory(models.Model):
    name = models.CharField(max_length=50)
    agent = models.OneToOneField('agents.Agent', related_name="memories", blank=True, null=True, on_delete=models.SET_NULL)
    schema = models.JSONField(null=True, blank=True, default=dict)
    data = models.JSONField(null=True, blank=True, default=dict)

    class Meta:
        verbose_name_plural = "Memories"

    def __str__(self):
        return f"Memory {self.name} - {self.agent}"
