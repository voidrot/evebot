from django.db import models


class InvUniqueName(models.Model):
    id = models.IntegerField(primary_key=True)
    group_id = models.IntegerField()
    item_name = models.TextField()

    def __str__(self):
        return f"{self.id}"
