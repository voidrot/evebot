from django.db import models


class IconID(models.Model):
    id = models.IntegerField(primary_key=True)
    obsolete = models.BooleanField(default=False, null=True, blank=True)
    description = models.TextField(null=True, default=None)  # noqa: DJ001
    icon_file = models.TextField()

    def __str__(self):
        return f"{self.id}"
