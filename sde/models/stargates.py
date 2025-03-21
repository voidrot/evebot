from django.db import models


class Stargate(models.Model):
    id = models.IntegerField(primary_key=True)
    type_id = models.IntegerField()
    destination = models.IntegerField()
    solar_system_id = models.IntegerField()
    position = models.JSONField(default=list)

    def __str__(self):
        return f"{self.id}"
