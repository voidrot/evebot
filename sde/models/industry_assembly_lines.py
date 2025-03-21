from django.db import models


class IndustryAssemblyLine(models.Model):
    id = models.IntegerField(primary_key=True)
    activity_id = models.IntegerField()
    base_material_multiplier = models.FloatField()
    base_time_multiplier = models.FloatField()
    name = models.TextField()
    description = models.TextField()
    details_per_group = models.JSONField(default=list)
    details_per_category = models.JSONField(default=list)

    def __str__(self):
        return f"{self.name}"
