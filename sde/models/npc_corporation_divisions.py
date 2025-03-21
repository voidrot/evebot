from django.db import models


class NPCCorporationDivision(models.Model):
    id = models.IntegerField(primary_key=True)
    description = models.TextField(null=True, default=None)  # noqa: DJ001
    internal_name = models.TextField()
    leader_type_name_id = models.JSONField()
    name_id = models.JSONField()
    description_id = models.JSONField(default=dict, null=True, blank=True)

    def __str__(self):
        return f"{self.name_id['en']}"
