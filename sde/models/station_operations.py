from django.db import models


class StationOperation(models.Model):
    id = models.IntegerField(primary_key=True)
    activity_id = models.IntegerField()
    border = models.FloatField()
    corridor = models.FloatField()
    description_id = models.JSONField(default=dict, null=True, blank=True)
    fringe = models.FloatField()
    hub = models.FloatField()
    manufacturing_factor = models.FloatField()
    operation_name_id = models.JSONField()
    ratio = models.FloatField()
    research_factor = models.FloatField()
    services = models.JSONField()
    station_types = models.JSONField(default=dict, null=True, blank=True)

    def __str__(self):
        return f"{self.id}"
