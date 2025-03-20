from django.db import models


class StationService(models.Model):
    id = models.IntegerField(primary_key=True)
    service_name_id = models.JSONField()
    description_id = models.JSONField(default=dict, null=True, blank=True)

    def __str__(self):
        return f"{self.id}"
