from django.db import models


class DogmaAttribute(models.Model):
    id = models.IntegerField(primary_key=True)
    category_id = models.IntegerField(default=None, null=True, blank=True)
    data_type = models.IntegerField()
    default_value = models.FloatField()
    description = models.TextField(null=True, default=None)
    high_is_good = models.BooleanField()
    name = models.TextField()
    published = models.BooleanField()
    stackable = models.BooleanField()
    display_name_id = models.JSONField(default=dict, null=True, blank=True)
    icon_id = models.IntegerField(default=None, null=True, blank=True)
    tooltip_description_id = models.JSONField(default=dict, null=True, blank=True)
    tooltip_title_id = models.JSONField(default=dict, null=True, blank=True)
    unit_id = models.IntegerField(default=None, null=True, blank=True)
    charge_recharge_time_id = models.IntegerField(default=None, null=True, blank=True)
    max_attribute_id = models.IntegerField(default=None, null=True, blank=True)
    min_attribute_id = models.IntegerField(default=None, null=True, blank=True)
    display_when_zero = models.BooleanField(default=False, null=True, blank=True)

    def __str__(self):
        return f"{self.id}"
