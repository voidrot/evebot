from django.db import models


class Star(models.Model):
    id = models.IntegerField(primary_key=True)
    type_id = models.IntegerField()
    age = models.BigIntegerField()
    life = models.BigIntegerField()
    locked = models.BooleanField()
    luminosity = models.FloatField()
    radius = models.FloatField()
    temperature = models.FloatField()
    constellation_id = models.IntegerField()
    region_id = models.IntegerField()
    solar_system_id = models.IntegerField()
    spectral_class = models.TextField()

    def __str__(self):
        return f"{self.id}"
