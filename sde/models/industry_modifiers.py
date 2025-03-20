from django.db import models


class IndustryModifier(models.Model):
    id = models.IntegerField(primary_key=True)
    manufacturing = models.JSONField(default=dict, null=True, blank=True)
    research_material = models.JSONField(default=dict, null=True, blank=True)
    research_time = models.JSONField(default=dict, null=True, blank=True)
    invention = models.JSONField(default=dict, null=True, blank=True)
    copying = models.JSONField(default=dict, null=True, blank=True)
    reaction = models.JSONField(default=dict, null=True, blank=True)

    def __str__(self):
        return f"{self.id}"
