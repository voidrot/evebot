from django.db import models


class InvItem(models.Model):
    id = models.IntegerField(primary_key=True)
    flag_id = models.IntegerField()
    item_id = models.IntegerField()
    location_id = models.IntegerField()
    owner_id = models.IntegerField()
    quantity = models.IntegerField()
    type_id = models.IntegerField()

    def __str__(self):
        return f"{self.id}"
