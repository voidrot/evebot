from django.db import models


class MetaGroup(models.Model):
    id = models.IntegerField(primary_key=True)
    icon_id = models.IntegerField(default=None, null=True, blank=True)
    color = models.JSONField(default=list, null=True, blank=True)
    name_id = models.JSONField()
    icon_suffix = models.TextField(null=True, default=None)  # noqa: DJ001
    description_id = models.JSONField(default=dict, null=True, blank=True)

    def __str__(self):
        return f"{self.name_id['en']}"
