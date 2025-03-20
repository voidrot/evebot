from django.db import models


class InvItem(models.Model):
    id = models.IntegerField(primary_key=True)
    location_id = models.IntegerField(null=True, default=None)
    owner_id = models.IntegerField()
    quantity = models.IntegerField()
    type_id = models.IntegerField()

    def __str__(self):
        return f"{self.id}"
