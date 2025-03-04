from django.db import models

class Item(models.Model):
    id = models.IntegerField(primary_key=True)
    flag_id = models.IntegerField()
    location_id = models.IntegerField()
    owner_id = models.IntegerField()
    quantity = models.IntegerField()
    type_id = models.IntegerField()
