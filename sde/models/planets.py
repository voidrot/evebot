from django.db import models


class Planet(models.Model):
    id = models.IntegerField(primary_key=True)
    celestial_index = models.IntegerField()
    planet_attributes = models.JSONField(default=dict)
    position = models.JSONField(default=dict)
    radius = models.IntegerField()
    statistics = models.JSONField(default=dict)
    type_id = models.IntegerField()

    def __str__(self):
        return f"{self.id}"
