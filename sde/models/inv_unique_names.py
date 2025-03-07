from django.db import models


class UniqueName(models.Model):
    id = models.IntegerField(primary_key=True)
    group_id = models.IntegerField()
    name = models.CharField(max_length=100)
