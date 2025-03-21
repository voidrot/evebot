from django.db import models


class Moon(models.Model):
    id = models.IntegerField(primary_key=True)
    planet_id = models.IntegerField()
    solar_system_id = models.IntegerField()
    region_id = models.IntegerField()
    constellation_id = models.IntegerField()
    radius = models.IntegerField()
    type_id = models.IntegerField()
    moon_attributes = models.JSONField(default=dict)
    position = models.JSONField(default=dict)
    statistics = models.JSONField(default=dict)

    def __str__(self):
        return f"{self.id}"
