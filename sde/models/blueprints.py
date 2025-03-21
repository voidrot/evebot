from django.db import models


class Blueprint(models.Model):
    id = models.IntegerField(primary_key=True)
    blueprint_type_id = models.IntegerField()
    max_production_limit = models.IntegerField()
    activities = models.JSONField(default=dict)

    def __str__(self):
        return f"{self.id}"
