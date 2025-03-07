from django.db import models


class Position(models.Model):
    item_id = models.IntegerField(primary_key=True)
    pitch = models.FloatField()
    roll = models.FloatField()
    x = models.FloatField()
    y = models.FloatField()
    z = models.FloatField()
    yaw = models.FloatField()
