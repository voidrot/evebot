from django.db import models


class DogmaEffect(models.Model):
    id = models.IntegerField(primary_key=True)
    disallow_auto_repeat = models.BooleanField()
    discharge_attribute_id = models.IntegerField(default=None, null=True, blank=True)
    duration_attribute_id = models.IntegerField(default=None, null=True, blank=True)
    effect_category = models.IntegerField()
    effect_id = models.IntegerField()
    effect_name = models.TextField()
    electronic_chance = models.BooleanField()
    guid = models.TextField(null=True, default=None)
    is_assistance = models.BooleanField()
    is_offensive = models.BooleanField()
    is_warp_safe = models.BooleanField()
    propulsion_chance = models.BooleanField()
    published = models.BooleanField()
    range_chance = models.BooleanField()
    distribution = models.IntegerField(default=None, null=True, blank=True)
    falloff_attribute_id = models.IntegerField(default=None, null=True, blank=True)
    range_attribute_id = models.IntegerField(default=None, null=True, blank=True)
    tracking_speed_attribute_id = models.IntegerField(
        default=None, null=True, blank=True
    )
    description_id = models.JSONField(default=dict, null=True, blank=True)
    display_name_id = models.JSONField(default=dict, null=True, blank=True)
    icon_id = models.IntegerField(default=None, null=True, blank=True)
    modifier_info = models.JSONField(default=list, null=True, blank=True)
    sfx_name = models.TextField(null=True, default=None)
    npc_usage_chance_attribute_id = models.IntegerField(
        default=None, null=True, blank=True
    )
    npc_activation_chance_attribute_id = models.IntegerField(
        default=None, null=True, blank=True
    )
    fitting_usage_chance_attribute_id = models.IntegerField(
        default=None, null=True, blank=True
    )
    resistance_attribute_id = models.IntegerField(default=None, null=True, blank=True)

    def __str__(self):
        return f"{self.id}"
