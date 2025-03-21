from django.db import models


class Constellation(models.Model):
    id = models.IntegerField(primary_key=True)
    region_id = models.IntegerField()
    name_id = models.IntegerField()
    radius = models.FloatField(null=True, default=None)
    name = models.TextField()
    center = models.JSONField()
    max = models.JSONField()
    min = models.JSONField()
    archetype = models.TextField()

    def __str__(self):
        return f"{self.name_id['en']}"
