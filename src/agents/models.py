from django.db import models

# Create your models here.
class Agent(models.Model):
    name = models.CharField(max_length=50)
    settings = models.JSONField(null=True, blank=True)
