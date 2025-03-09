from django.db import models


class PlanetSchematic(models.Model):
    id = models.IntegerField(primary_key=True)
    cycle_time = models.IntegerField()
    name_id = models.JSONField()
    pins = models.JSONField()
    types = models.JSONField()

    def __str__(self):
        return f"{self.name_id["en"]}"
