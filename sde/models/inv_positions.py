from django.db import models


class InvPosition(models.Model):
    id = models.IntegerField(primary_key=True)
    pitch = models.FloatField(default=None, null=True, blank=True)
    roll = models.FloatField(default=None, null=True, blank=True)
    x = models.FloatField()
    y = models.FloatField()
    yaw = models.FloatField(default=None, null=True, blank=True)
    z = models.FloatField()

    def __str__(self):
        return f"{self.id}"
