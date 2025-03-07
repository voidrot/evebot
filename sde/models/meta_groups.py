from django.db import models


class MetaGroup(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.TextField()
    description = models.TextField(null=True, blank=True, default=None)
    icon_id = models.IntegerField(null=True, blank=True, default=None)
    icon_suffix = models.TextField(null=True, blank=True, default=None)
    color_r = models.FloatField()
    color_g = models.FloatField()
    color_b = models.FloatField()
    color_alpha = models.FloatField()
