from django.db import models


class SolarSystem(models.Model):
    id = models.IntegerField(primary_key=True)
    border = models.BooleanField()
    center = models.JSONField()
    corridor = models.BooleanField()
    fringe = models.BooleanField()
    hub = models.BooleanField()
    international = models.BooleanField()
    luminosity = models.FloatField()
    max = models.JSONField()
    min = models.JSONField()
    radius = models.FloatField()
    regional = models.BooleanField()
    security = models.FloatField()
    solar_system_id = models.IntegerField()
    solar_system_name_id = models.IntegerField()
    star_id = models.IntegerField()
    sun_type_id = models.IntegerField()

    def __str__(self):
        return f"{self.id}"
