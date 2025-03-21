from django.db import models


class Planet(models.Model):
    id = models.IntegerField(primary_key=True)
    celestial_index = models.IntegerField()
    radius = models.IntegerField()
    type_id = models.IntegerField()
    constellation_id = models.IntegerField()
    region_id = models.IntegerField()
    solar_system_id = models.IntegerField()
    planet_attributes = models.JSONField(default=dict)
    position = models.JSONField(default=list)
    statistics = models.JSONField(default=dict)

    def __str__(self):
        return f"{self.id}"
