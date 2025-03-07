from django.db import models


class MarketGroup(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.TextField()
    description = models.TextField()
    has_types = models.BooleanField(default=False)
    parent_group_id = models.IntegerField(null=True, blank=True, default=None)
