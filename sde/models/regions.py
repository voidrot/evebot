from django.db import models


class Region(models.Model):
    id = models.IntegerField(primary_key=True)
    description_id = models.IntegerField(null=True, default=None)
    faction_id = models.IntegerField(null=True, default=None)
    name_id = models.IntegerField()
    nebula = models.IntegerField()
    wormhole_class_id = models.IntegerField(null=True, default=None)
    name = models.TextField()
    center = models.JSONField()
    max = models.JSONField()
    min = models.JSONField()
    archetype = models.TextField()

    def __str__(self):
        return f"{self.name_id['en']}"
