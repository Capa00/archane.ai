from djongo import models

class Interest(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        abstract = True

class TargetAudience(models.Model):
    age_range = models.JSONField()
    interests = models.ArrayField(
        model_container=Interest,
        blank=True,
    )
    locations = models.ArrayField(
        model_container=Interest,
        blank=True,
    )

    class Meta:
         abstract = False