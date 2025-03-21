from django.db import models


class StationOperation(models.Model):
    id = models.IntegerField(primary_key=True)
    activity_id = models.IntegerField()
    border = models.FloatField()
    corridor = models.FloatField()
    fringe = models.FloatField()
    hub = models.FloatField()
    manufacturing_factor = models.FloatField()
    ratio = models.FloatField()
    research_factor = models.FloatField()
    description_id = models.JSONField(default=dict, null=True, blank=True)
    operation_name_id = models.JSONField()
    services = models.JSONField()
    station_types = models.JSONField(default=dict, null=True, blank=True)

    def __str__(self):
        return f"{self.id}"
