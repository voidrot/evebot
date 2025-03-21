from django.db import models


class Skin(models.Model):
    id = models.IntegerField(primary_key=True)
    allow_ccpdevs = models.BooleanField()
    skin_id = models.IntegerField()
    skin_material_id = models.IntegerField()
    visible_serenity = models.BooleanField()
    visible_tranquility = models.BooleanField()
    is_structure_skin = models.BooleanField(default=False, null=True, blank=True)
    internal_name = models.TextField()
    types = models.JSONField()
    skin_description = models.TextField(null=True, default=None)  # noqa: DJ001

    def __str__(self):
        return f"{self.id}"
