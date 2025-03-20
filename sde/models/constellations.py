from django.db import models


class Constellation(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.TextField()
    center = models.JSONField()
    region_id = models.IntegerField()
    max = models.JSONField()
    min = models.JSONField()
    name_id = models.IntegerField()
    radius = models.FloatField(null=True, default=None)
    archetype = models.TextField()

    def __str__(self):
        return f"{self.name_id['en']}"
