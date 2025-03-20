from django.db import models

class IndustryAssemblyLine(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.TextField()
    description = models.TextField()
    activity_id = models.IntegerField()
    base_material_multiplier = models.FloatField()
    base_time_multiplier = models.FloatField()
    details_per_group = models.JSONField(default=list)
    details_per_category = models.JSONField(default=list)
