from django.db import models


class ExpertSystem(models.Model):
    id = models.IntegerField(primary_key=True)
    hidden = models.BooleanField()
    duration_days = models.IntegerField()
    retired = models.BooleanField()
    name = models.TextField()
    skills_granted = models.JSONField(default=dict)
    associated_ship_types = models.JSONField(default=list)

    def __str__(self):
        return f"{self.name}"
