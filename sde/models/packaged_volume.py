from django.db import models


class PackagedVolume(models.Model):
    id = models.IntegerField(primary_key=True)
    packaged_volume = models.IntegerField()
    group_name = models.TextField()

    def __str__(self):
        return f"{self.id}"
