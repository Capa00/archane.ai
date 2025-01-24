from django.db.models import JSONField
from djongo import models

class Interest(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        abstract = True

class TargetAudience(models.Model):
    age_range = JSONField(null=True, blank=True, default={})
    interests = JSONField(null=True, blank=True, default=[])
    locations = JSONField(null=True, blank=True, default=[])

    class Meta:
         abstract = False