from django.db import models


class NPCCorporationDivision(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.TextField()
    description = models.TextField(null=True, blank=True, default=None)
    internal_name = models.TextField(null=True, blank=True, default=None)
    leader_type_name = models.TextField(null=True, blank=True, default=None)
    description_long = models.TextField(null=True, blank=True, default=None)
