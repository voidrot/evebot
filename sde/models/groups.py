from django.db import models


class Group(models.Model):
    id = models.IntegerField(primary_key=True)
    anchorable = models.BooleanField()
    anchored = models.BooleanField()
    category_id = models.IntegerField()
    fittable_non_singleton = models.BooleanField()
    published = models.BooleanField()
    use_base_price = models.BooleanField()
    icon_id = models.IntegerField(default=None, null=True, blank=True)
    name = models.JSONField()

    def __str__(self):
        return f"{self.id}"
