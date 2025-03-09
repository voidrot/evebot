from django.db import models


class IconId(models.Model):
    id = models.IntegerField(primary_key=True)
    description = models.TextField(default=None)
    icon_file = models.TextField()
    obsolete = models.BooleanField(default=False, null=True, blank=True)

    def __str__(self):
        return f"{self.id}"
