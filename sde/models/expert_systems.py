from django.db import models


class ExpertSystem(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.TextField()
    hidden = models.BooleanField()
    duration_days = models.IntegerField()
    skills_granted = models.JSONField(default=dict)
    associated_ship_types = models.JSONField(default=list)
    retired = models.BooleanField()

    def __str__(self):
        return f"{self.name}"
