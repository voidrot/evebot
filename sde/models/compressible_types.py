from django.db import models


class CompressibleType(models.Model):
    id = models.IntegerField(primary_key=True)
    type_id = models.IntegerField()
