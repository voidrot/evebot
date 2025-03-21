from django.db import models


class InvFlag(models.Model):
    id = models.IntegerField(primary_key=True)
    order_id = models.IntegerField()
    flag_name = models.TextField()
    flag_text = models.TextField()

    def __str__(self):
        return f"{self.id}"
