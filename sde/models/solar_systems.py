from django.db import models


class SolarSystem(models.Model):
    id = models.IntegerField(primary_key=True)
    constellation_id = models.IntegerField()
    region_id = models.IntegerField()
    border = models.BooleanField()
    corridor = models.BooleanField()
    fringe = models.BooleanField()
    hub = models.BooleanField()
    international = models.BooleanField()
    luminosity = models.FloatField()
    radius = models.FloatField()
    regional = models.BooleanField()
    security = models.FloatField()
    star_id = models.IntegerField(null=True, default=None)
    sun_type_id = models.IntegerField(null=True, default=None)
    name = models.TextField()
    center = models.JSONField(default=list)
    max = models.JSONField(default=list)
    min = models.JSONField(default=list)
    secondary_sun = models.JSONField(default=dict, null=True)
    archetype = models.TextField()

    def __str__(self):
        return f"{self.id}"
