from django.db import models

class Position(models.Model):
    item_id = models.IntegerField(primary_key=True)
    pitch = models.DecimalField()
    roll = models.DecimalField()
    x = models.DecimalField()
    y = models.DecimalField()
    z = models.DecimalField()
    yaw = models.DecimalField()
