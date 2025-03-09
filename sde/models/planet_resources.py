from django.db import models


class PlanetResource(models.Model):
    id = models.IntegerField(primary_key=True)
    power = models.IntegerField(default=None, null=True, blank=True)
    workforce = models.IntegerField(default=None, null=True, blank=True)
    cycle_minutes = models.IntegerField(default=None, null=True, blank=True)
    harvest_silo_max = models.IntegerField(default=None, null=True, blank=True)
    maturation_cycle_minutes = models.IntegerField(default=None, null=True, blank=True)
    maturation_percent = models.IntegerField(default=None, null=True, blank=True)
    mature_silo_max = models.FloatField(default=None, null=True, blank=True)
    reagent_harvest_amount = models.IntegerField(default=None, null=True, blank=True)
    reagent_type_id = models.IntegerField(default=None, null=True, blank=True)

    def __str__(self):
        return f"{self.id}"
