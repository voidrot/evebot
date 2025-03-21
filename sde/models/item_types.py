from django.db import models


class Type(models.Model):
    id = models.IntegerField(primary_key=True)
    group_id = models.IntegerField()
    mass = models.FloatField(default=None, null=True, blank=True)
    name = models.JSONField()
    portion_size = models.IntegerField()
    published = models.BooleanField()
    volume = models.FloatField(default=None, null=True, blank=True)
    radius = models.FloatField(default=None, null=True, blank=True)
    graphic_id = models.IntegerField(default=None, null=True, blank=True)
    sound_id = models.IntegerField(default=None, null=True, blank=True)
    icon_id = models.IntegerField(default=None, null=True, blank=True)
    race_id = models.IntegerField(default=None, null=True, blank=True)
    base_price = models.FloatField(default=None, null=True, blank=True)
    market_group_id = models.IntegerField(default=None, null=True, blank=True)
    capacity = models.FloatField(default=None, null=True, blank=True)
    meta_group_id = models.IntegerField(default=None, null=True, blank=True)
    variation_parent_type_id = models.IntegerField(default=None, null=True, blank=True)
    faction_id = models.IntegerField(default=None, null=True, blank=True)
    sof_material_set_id = models.IntegerField(default=None, null=True, blank=True)
    description = models.JSONField(default=dict, null=True, blank=True)
    sof_faction_name = models.TextField(null=True, default=None)  # noqa: DJ001
    masteries = models.JSONField(default=dict, null=True, blank=True)
    traits = models.JSONField(default=dict, null=True, blank=True)

    def __str__(self):
        return f"{self.id}"
