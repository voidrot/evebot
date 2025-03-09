from django.db import models


class Category(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.JSONField()
    published = models.BooleanField()
    icon_id = models.IntegerField(default=None, null=True, blank=True)

    def __str__(self):
        return f"{self.id}"
