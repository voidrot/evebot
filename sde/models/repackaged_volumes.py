from django.db import models

class RepackagedVolume(models.Model):
    item_id = models.IntegerField(primary_key=True)
    volume = models.FloatField()

    def __str__(self):
        return f"{self.item_id}"
