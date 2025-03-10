from django.db import models


class InvName(models.Model):
    id = models.IntegerField(primary_key=True)
    item_name = models.TextField()

    def __str__(self):
        return f"{self.id}"
