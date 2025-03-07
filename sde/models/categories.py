from django.db import models


class Category(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.TextField()
    icon_id = models.IntegerField(null=True, blank=True, default=None)
    published = models.BooleanField(default=False)
