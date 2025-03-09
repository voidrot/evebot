from django.db import models


class Region(models.Model):
    id = models.IntegerField(primary_key=True)
    center = models.JSONField()
    description_id = models.IntegerField()
    faction_id = models.IntegerField()
    max = models.JSONField()
    min = models.JSONField()
    name_id = models.IntegerField()
    nebula = models.IntegerField()
    region_id = models.IntegerField()

    def __str__(self):
        return f"{self.name_id["en"]}"
