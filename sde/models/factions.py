from django.db import models


class Faction(models.Model):
    id = models.IntegerField(primary_key=True)
    corporation_id = models.IntegerField(default=None, null=True, blank=True)
    description_id = models.JSONField()
    flat_logo = models.TextField(null=True, default=None)
    flat_logo_with_name = models.TextField(null=True, default=None)
    icon_id = models.IntegerField()
    member_races = models.JSONField()
    militia_corporation_id = models.IntegerField(default=None, null=True, blank=True)
    name_id = models.JSONField()
    short_description_id = models.JSONField(default=dict, null=True, blank=True)
    size_factor = models.FloatField()
    solar_system_id = models.IntegerField()
    unique_name = models.BooleanField()

    def __str__(self):
        return f"{self.name_id['en']}"
