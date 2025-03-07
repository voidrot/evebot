from django.db import models


class Group(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.TextField()
    anchorable = models.BooleanField(default=False)
    anchored = models.BooleanField(default=False)
    category_id = models.IntegerField()
    fittable_non_singleton = models.BooleanField(default=False)
    icon_id = models.IntegerField()
    use_base_price = models.BooleanField(default=False)
    published = models.BooleanField(default=False)
