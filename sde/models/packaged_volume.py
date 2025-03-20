from django.db import models


class PackagedVolume(models.Model):
    id = models.IntegerField(primary_key=True)
    group_name = models.TextField()
    packaged_volume = models.IntegerField()

    def __str__(self):
        return f"{self.id}"
