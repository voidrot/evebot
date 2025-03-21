from django.db import models


class IndustryInstallationType(models.Model):
    id = models.IntegerField(primary_key=True)
    assembly_lines = models.JSONField(default=list)
