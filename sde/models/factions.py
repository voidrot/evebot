from django.db import models


class Faction(models.Model):
    id = models.IntegerField(primary_key=True)
    corporation_id = models.IntegerField(default=None, null=True, blank=True)
    icon_id = models.IntegerField()
    militia_corporation_id = models.IntegerField(default=None, null=True, blank=True)
    size_factor = models.FloatField()
    solar_system_id = models.IntegerField()
    unique_name = models.BooleanField()
    description_id = models.JSONField()
    flat_logo = models.TextField(null=True, default=None)  # noqa: DJ001
    flat_logo_with_name = models.TextField(null=True, default=None)  # noqa: DJ001
    member_races = models.JSONField()
    name_id = models.JSONField()
    short_description_id = models.JSONField(default=dict, null=True, blank=True)

    def __str__(self):
        return f"{self.name_id['en']}"
