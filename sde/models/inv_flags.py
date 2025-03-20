from django.db import models


class InvFlag(models.Model):
    id = models.IntegerField(primary_key=True)
    flag_name = models.TextField()
    flag_text = models.TextField()
    order_id = models.IntegerField()

    def __str__(self):
        return f"{self.id}"
