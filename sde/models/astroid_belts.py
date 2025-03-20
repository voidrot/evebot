from django.db import models


class AsteroidBelt(models.Model):
    id = models.IntegerField(primary_key=True)
    planet_id = models.IntegerField()
    solar_system_id = models.IntegerField()
    region_id = models.IntegerField()
    constellation_id = models.IntegerField()
    position = models.JSONField(default=list)
    statistics = models.JSONField(default=dict)
    type_id = models.IntegerField()

    def __str__(self):
        return f"{self.id}"
