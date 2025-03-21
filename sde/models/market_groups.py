from django.db import models


class MarketGroup(models.Model):
    id = models.IntegerField(primary_key=True)
    has_types = models.BooleanField()
    icon_id = models.IntegerField(default=None, null=True, blank=True)
    parent_group_id = models.IntegerField(default=None, null=True, blank=True)
    description_id = models.JSONField(default=dict, null=True, blank=True)
    name_id = models.JSONField()

    def __str__(self):
        return f"{self.name_id['en']}"
