from django.db import models

class Flag(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.TextField(max_length=50)
    name_long = models.CharField(max_length=85)
    order_id = models.IntegerField()
