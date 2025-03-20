from django.db import models


class ContrabandType(models.Model):
    id = models.IntegerField(primary_key=True)
    factions = models.JSONField()

    def __str__(self):
        return f"{self.id}"
